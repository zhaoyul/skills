#!/usr/bin/env bb

(babashka.deps/add-deps '{:deps {parinferish/parinferish {:mvn/version "0.8.0"}}})

(ns paren-lisp-repair
  (:require [babashka.fs :as fs]
            [clojure.string :as string]
            [parinferish.core :as parinferish]))

(def supported-extensions
  #{".el" ".elisp"
    ".scm" ".ss" ".sld" ".sls" ".rkt"
    ".lisp" ".lsp" ".cl" ".asd"
    ".sexp"})

(defn has-stdin-data? []
  (try
    (.ready *in*)
    (catch Exception _ false)))

(defn supported-file? [path]
  (contains? supported-extensions
             (some-> path fs/extension string/lower-case)))

(defn attempt-repair [input mode]
  (try
    {:success true
     :mode mode
     :text (-> input
               (parinferish/parse {:mode mode})
               parinferish/flatten)}
    (catch Exception e
      {:success false
       :mode mode
       :error (.getMessage e)})))

(defn repair-text [input]
  (let [indent-result (attempt-repair input :indent)]
    (if (:success indent-result)
      (assoc indent-result :changed (not= input (:text indent-result)))
      (let [paren-result (attempt-repair input :paren)]
        (if (:success paren-result)
          (assoc paren-result :changed (not= input (:text paren-result)))
          {:success false
           :error (or (:error paren-result)
                      (:error indent-result)
                      "Could not repair delimiters")})))))

(defn process-stdin []
  (let [input (slurp *in*)
        {:keys [success text error]} (repair-text input)]
    (if success
      (do
        (print text)
        (flush)
        0)
      (do
        (binding [*out* *err*]
          (println "Error:" error))
        1))))

(defn process-file [path force?]
  (cond
    (not (fs/exists? path))
    {:success false
     :path path
     :message "File does not exist"}

    (fs/directory? path)
    {:success false
     :path path
     :message "Path is a directory"}

    (and (not force?) (not (supported-file? path)))
    {:success false
     :path path
     :message "Unsupported file extension (use --force to override)"}

    :else
    (let [input (slurp path)
          {:keys [success text changed error mode]} (repair-text input)]
      (if success
        (do
          (when changed
            (spit path text))
          {:success true
           :path path
           :message (if changed
                      (str "Repaired with " (name mode) " mode")
                      "Already balanced")})
        {:success false
         :path path
         :message error}))))

(defn show-help []
  (println "Usage: paren-lisp-repair.bb [--force] [FILE ...]")
  (println "       cat broken.lisp | paren-lisp-repair.bb")
  (println)
  (println "Repair delimiter errors for Lisp-family files in place.")
  (println)
  (println "Options:")
  (println "  --force       Process files with unsupported extensions")
  (println "  -h, --help    Show this help message")
  (println)
  (println "Supported extensions:")
  (println "  .el .elisp .scm .ss .sld .sls .rkt .lisp .lsp .cl .asd .sexp"))

(defn parse-args [args]
  (loop [remaining args
         opts {:force? false
               :help? false
               :files []}]
    (if-let [arg (first remaining)]
      (case arg
        "--force" (recur (rest remaining) (assoc opts :force? true))
        "-h" (recur (rest remaining) (assoc opts :help? true))
        "--help" (recur (rest remaining) (assoc opts :help? true))
        (recur (rest remaining) (update opts :files conj arg)))
      opts)))

(defn print-file-results [results]
  (println)
  (println "paren-lisp-repair Results")
  (println "=========================")
  (println)
  (doseq [{:keys [path message]} results]
    (println (str "  " path ": " message)))
  (println)
  (println "Summary:")
  (println "  Success:" (count (filter :success results)))
  (println "  Failed: " (count (remove :success results)))
  (println))

(defn -main [& args]
  (let [{:keys [help? force? files]} (parse-args args)]
    (cond
      help?
      (do
        (show-help)
        (System/exit 0))

      (seq files)
      (let [results (mapv #(process-file % force?) files)]
        (print-file-results results)
        (System/exit (if (every? :success results) 0 1)))

      (has-stdin-data?)
      (System/exit (process-stdin))

      :else
      (do
        (show-help)
        (System/exit 1)))))

(apply -main *command-line-args*)
