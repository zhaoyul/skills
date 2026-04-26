#!/usr/bin/env bb

(ns paren-lisp-repair
  (:require [babashka.fs :as fs]
            [clojure.string :as string]))

(def supported-extensions
  #{"el" "elisp"
    "scm" "ss" "sld" "sls" "rkt"
    "lisp" "lsp" "cl" "asd"
    "sexp"})

(defn has-stdin-data? []
  (try
    (.ready *in*)
    (catch Exception _ false)))

(defn supported-file? [path]
  (contains? supported-extensions
             (some-> path fs/extension string/lower-case)))

(defn repair-text [input]
  (let [open->close {\( \) \[ \] \{ \}}
        close->open (zipmap (vals open->close) (keys open->close))
        chars (vec input)]
    (loop [idx 0
           out []
           stack []
           in-string? false
           escaped? false
           line-comment? false
           block-comment-depth 0
           char-literal? false
           changed? false]
      (if (= idx (count chars))
        {:success true
         :changed (or changed? (seq stack))
         :text (apply str (concat out (map open->close (reverse stack))))}
        (let [ch (nth chars idx)
              next-ch (when (< (inc idx) (count chars))
                        (nth chars (inc idx)))]
          (cond
            char-literal?
            (recur (inc idx) (conj out ch) stack in-string? false line-comment? block-comment-depth false changed?)

            (> block-comment-depth 0)
            (cond
              (and (= ch \#) (= next-ch \|))
              (recur (+ idx 2)
                     (conj out ch next-ch)
                     stack
                     in-string?
                     escaped?
                     line-comment?
                     (inc block-comment-depth)
                     false
                     changed?)

              (and (= ch \|) (= next-ch \#))
              (recur (+ idx 2)
                     (conj out ch next-ch)
                     stack
                     in-string?
                     escaped?
                     line-comment?
                     (dec block-comment-depth)
                     false
                     changed?)

              :else
              (recur (inc idx) (conj out ch) stack in-string? escaped? line-comment? block-comment-depth false changed?))

            line-comment?
            (recur (inc idx)
                   (conj out ch)
                   stack
                   in-string?
                   escaped?
                   (not= ch \newline)
                   block-comment-depth
                   false
                   changed?)

            in-string?
            (cond
              escaped?
              (recur (inc idx) (conj out ch) stack true false line-comment? block-comment-depth false changed?)

              (= ch \\)
              (recur (inc idx) (conj out ch) stack true true line-comment? block-comment-depth false changed?)

              (= ch \")
              (recur (inc idx) (conj out ch) stack false false line-comment? block-comment-depth false changed?)

              :else
              (recur (inc idx) (conj out ch) stack true false line-comment? block-comment-depth false changed?))

            (and (= ch \#) (= next-ch \|))
            (recur (+ idx 2)
                   (conj out ch next-ch)
                   stack
                   in-string?
                   escaped?
                   line-comment?
                   1
                   false
                   changed?)

            (= ch \;)
            (recur (inc idx) (conj out ch) stack in-string? escaped? true block-comment-depth false changed?)

            (= ch \")
            (recur (inc idx) (conj out ch) stack true false line-comment? block-comment-depth false changed?)

            (and (= ch \#) (= next-ch \\))
            (recur (+ idx 2)
                   (conj out ch next-ch)
                   stack
                   in-string?
                   escaped?
                   line-comment?
                   block-comment-depth
                   true
                   changed?)

            (contains? open->close ch)
            (recur (inc idx) (conj out ch) (conj stack ch) in-string? escaped? line-comment? block-comment-depth false changed?)

            (contains? close->open ch)
            (if-let [open (peek stack)]
              (let [expected (open->close open)]
                (recur (inc idx)
                       (conj out expected)
                       (pop stack)
                       in-string?
                       escaped?
                       line-comment?
                       block-comment-depth
                       false
                       (or changed? (not= ch expected))))
              (recur (inc idx) out stack in-string? escaped? line-comment? block-comment-depth false true))

            :else
            (recur (inc idx) (conj out ch) stack in-string? escaped? line-comment? block-comment-depth false changed?)))))))

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
          {:keys [success text changed error]} (repair-text input)]
      (if success
        (do
          (when changed
            (spit path text))
          {:success true
           :path path
           :message (if changed
                      "Repaired delimiters"
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
