---
name: clojuredart-dev
description: Help build, debug, refactor, test, and review ClojureDart applications that target Flutter, native mobile/desktop, web, or plain Dart. Use when the user asks about ClojureDart, .cljd files, cljd.build, deps.edn :cljd/opts, cljd.flutter, Dart package interop from Clojure syntax, Flutter widget construction in ClojureDart, hot reload, REPL, or ClojureDart testing.
---

# ClojureDart Development Skill

Use this skill to act as a practical ClojureDart pair programmer. Optimize for working code, idiomatic ClojureDart, and Flutter/Dart interop correctness.

ClojureDart is not just Clojure syntax pasted over Flutter. Treat it as a Clojure dialect hosted on Dart, with Dart's stronger type and runtime model shaping interop, constructors, named arguments, static properties, nullability, generics, and widget lifecycles.

## Default response style

- Match the user's language. If the user writes Chinese, answer in Simplified Chinese unless they ask otherwise.
- Prefer complete, runnable code over fragments.
- When editing code, show full files or full relevant namespaces unless the user explicitly asks for a small diff.
- Do not invent APIs. If a symbol, package, widget, or macro is uncertain, say so and inspect available project files or documentation when possible.
- For application work, consider both the ClojureDart layer and generated Dart/Flutter behavior.
- Explain ClojureDart-specific syntax briefly when it differs from JVM Clojure or ClojureScript.

## First-pass project discovery

When the user provides a repository, files, or a working tree, inspect these before making design claims:

1. `deps.edn`
   - `:deps` entry for `tensegritics/clojuredart` or local checkout.
   - `:aliases`, especially `:cljd`, `:test`, `:dev`, or app-specific aliases.
   - `:cljd/opts`, especially `:kind`, `:main`, `:dart-test-args`, and output-related settings.
2. `pubspec.yaml`
   - Flutter SDK constraints.
   - Dart/Flutter packages used by ClojureDart namespaces.
   - Assets, fonts, platform plugin dependencies.
3. Source roots
   - Usually `src`, sometimes `test`, `integration_test`, sample-specific directories.
   - ClojureDart files usually end in `.cljd`.
4. Entry namespace
   - The namespace named by `:cljd/opts {:main ...}` should define `(defn main [] ...)`.
5. Generated/native folders
   - `android`, `ios`, `macos`, `linux`, `windows`, `web` are Flutter platform folders. Avoid hand-editing generated files unless the task is platform integration.
6. Test namespaces
   - Look for `cljd.test`, `dart test` usage, widget test runners, and tags.

If no files are available, provide a minimal project skeleton and ask for the specific error or file only when needed.

## Canonical commands

Use these commands as the basic operating model:

```sh
clj -M:cljd init
clj -M:cljd flutter
clj -M:cljd compile
clj -M:cljd clean
clj -M:cljd upgrade
clj -M:cljd test
```

Typical command meanings:

- `init`: initialize Flutter/Dart project artifacts for a ClojureDart project.
- `flutter`: compile, watch, and hot reload. Press return in the watcher to force restart when hot reload does not pick up changes.
- `compile`: ahead-of-time compilation for deployment-oriented builds.
- `clean`: clear generated or stale build state.
- `upgrade`: update an existing project to the current ClojureDart revision.
- `test`: compile test namespaces and run through Dart testing tooling.

When troubleshooting, ask for or inspect the command output. ClojureDart failures may come from Clojure compilation, Dart analysis/compile, Flutter tooling, platform setup, or package resolution. Keep these layers separate.

## Minimal Flutter app skeleton

Use this as the baseline when the user asks to start a ClojureDart Flutter app.

`deps.edn`:

```clojure
{:paths ["src"]
 :deps {tensegritics/clojuredart
        {:git/url "https://github.com/tensegritics/ClojureDart.git"
         ;; Pin this to the revision required by the project.
         :sha "<clojuredart-sha>"}}
 :aliases {:cljd {:main-opts ["-m" "cljd.build"]}}
 :cljd/opts {:kind :flutter
             :main acme.main}}
```

`src/acme/main.cljd`:

```clojure
(ns acme.main
  (:require ["package:flutter/material.dart" :as m]
            [cljd.flutter :as f]))

(defn main []
  (f/run
    (m/MaterialApp
      .title "Welcome to ClojureDart"
      .theme (m/ThemeData .primarySwatch m/Colors/pink))
    .home
    (m/Scaffold
      .appBar (m/AppBar
                .title (m/Text "ClojureDart")))
    .body
    m/Center
    (m/Text "Let's get coding!"
      .style (m/TextStyle
               .fontSize 32.0))))
```

Then initialize and run:

```sh
clj -M:cljd init
clj -M:cljd flutter
```

## ClojureDart interop rules to protect

### Dart packages in `ns`

Dart package imports use strings in `:require`:

```clojure
(ns my.project
  (:require ["package:flutter/material.dart" :as m]
            [cljd.flutter :as f]))
```

Prefer short aliases that match examples and docs, such as `m` for Material and `f` for `cljd.flutter`.

### Constructors

Do not write Java-style `new` or trailing-dot constructors. Put the Dart class in function position:

```clojure
(StringBuffer "hello")
(m/Text "Hello")
(m/Scaffold .body (m/Text "Body"))
```

Named constructors are called like static methods:

```clojure
(List/empty .growable true)
```

### Named arguments

Dart named arguments become dotted names:

```clojure
(m/Text "Hello world"
  .maxLines 2
  .softWrap true
  .overflow m/TextOverflow.fade)
```

Do not convert these to maps unless a specific ClojureDart API expects a map.

### Static properties and enums

Static properties are accessed through the alias/type path:

```clojure
m/Colors.purple
m/Colors.purple.shade900
m/TextAlign.left
```

### Instance property access

Get properties with `.-prop`:

```clojure
(.-height size)
```

Set properties with `.-prop!` or `set!`:

```clojure
(.-value! controller "new text")
(set! (.-value controller) "new text")
```

### Object destructuring with `:flds`

Use `:flds` for Dart object fields/properties:

```clojure
(let [{:flds [height width]} size]
  ...)
```

### Nullability and type hints

ClojureDart type hints encode Dart nullability:

```clojure
(defn greet [^String name] ... )   ; non-null String
(defn maybe [^String? name] ... )  ; nullable String
```

### Generics

Dart generics are runtime-visible. ClojureDart represents parameterized types with `#/` metadata-style syntax:

```clojure
^#/(List Map) x
```

Use this when a Dart API needs precise generic type information.

### Optional and named parameters in function signatures

When implementing callbacks or methods that accept Dart optional params:

```clojure
[a b c .d .e]       ; three positional params, two optional named params
[a b c ... d e]     ; three fixed positional params, two optional positional params
[.a 42 .e]          ; named params, with a default for a
[... a 42 b]        ; optional positional params, with a default for a
```

## `cljd.flutter` idioms

`cljd.flutter` reduces Flutter boilerplate. Prefer it for user-facing UI code unless the project intentionally avoids it.

Always consider:

- `f/run` for the app entry point.
- `f/widget` for building widgets with ClojureDart-friendly directives.
- Child threading in widget bodies.
- `:let` for local bindings inside widget bodies.
- `:key` for preserving sibling widget identity.
- `:watch` for state, futures, streams, listenables, atoms, and reactive UI updates.
- `:managed` for lifecycle-managed objects requiring disposal or refresh.
- `:bind`, `:get`, `:context`, `:vsync`, `:when`, `:padding`, `:height`, `:width`, and `:color` when they simplify widget code.

Child threading example:

```clojure
(f/widget
  m/MaterialApp
  .home
  m/Scaffold
  .body
  m/Center
  (m/Text "Hello"))
```

This means nested `.home`, `.body`, and `.child` composition. Preserve this style in refactors instead of flattening every widget manually.

Reactive UI example:

```clojure
(f/widget
  :watch [v an-atom]
  (m/Text (str v)))
```

When the watchable changes, the widget body after `:watch` updates.

## Testing workflow

ClojureDart tests use `cljd.test`, a `clojure.test`-style port built on Dart's test tooling.

Basic command:

```sh
clj -M:cljd test
```

Pass Dart test flags after `--`:

```sh
clj -M:cljd test -- -t widget
```

For extra test paths, combine aliases:

```sh
clj -M:test:cljd test
```

Widget-test shape:

```clojure
(deftest renders-title
  :tags [:widget]
  :runner (ft/testWidgets [tester])
  (let [^ft/WidgetTester {:flds [pumpWidget]} tester
        _ (await (pumpWidget (my-widget "Title")))
        title-finder (ft/find.text "Title")]
    (ft/expect title-finder ft/findsOneWidget)))
```

When writing tests:

- Keep pure logic tests separate from widget tests.
- Tag widget tests so `dart test -t widget` selection remains useful.
- Use `:dart.test/dir` metadata for integration tests that should compile into `integration_test`.
- Explain whether `--` replaces alias-level Dart test args or `++` should append, when relevant.

## REPL and hot reload workflow

The watcher may print a socket REPL port. It is a socket REPL, not nREPL. The REPL relies on Dart hot reload, so evaluation can lag depending on namespace and dependency graph.

Useful REPL concepts:

- Connect with a socket client such as `nc localhost <port>`.
- `*1`, `*2`, `*3`, and `*e` are available.
- `*env` becomes useful after using `cljd.flutter.repl/pick!`; it exposes lexical bindings and build context for the selected widget.
- `cljd.flutter.repl/mount!` can replace a selected widget and stores the replaced widget in `*1`.

When a user reports hot reload confusion, distinguish:

- ClojureDart watcher compiling successfully but Flutter not refreshing.
- Flutter hot reload limitations.
- Needing to press return in the watcher for restart.
- Needing `clj -M:cljd clean` after stale generated state.

## Debugging decision tree

When the user pastes an error, classify it first:

1. `clj`, tools.deps, git dependency, alias, or `deps.edn` problem.
2. ClojureDart compile problem, such as namespace, macro, type hint, interop, or syntax.
3. Dart package import or `pubspec.yaml` problem.
4. Flutter platform/device problem.
5. Runtime Flutter/widget lifecycle problem.
6. Test runner problem.

Then respond with:

- The most likely layer.
- The smallest verification command.
- The exact file or form to change.
- A complete corrected code block when possible.

Common fixes:

- Missing Flutter Material symbols: check `[:require ["package:flutter/material.dart" :as m]]`.
- Named argument errors: convert Dart `name:` arguments to `.name` pairs.
- Constructor errors: remove `new` and trailing-dot constructor syntax.
- Property errors: use `.-prop`, `.-prop!`, or static property access correctly.
- Hot reload stale behavior: press return in watcher, then try `clj -M:cljd clean` if needed.
- Device target confusion: run `flutter devices`, then pass `-d <device-id>` to `clj -M:cljd flutter`.

## Code review checklist

For every ClojureDart code review, check:

- Namespace imports use strings for Dart packages.
- Aliases are clear and consistent.
- `deps.edn` has a valid `:cljd` alias and correct `:cljd/opts`.
- `main` namespace exists and defines `main`.
- Named args are dotted `.arg value` pairs.
- Constructors are class calls, not JVM-style `new` calls.
- Widget trees preserve idiomatic `f/widget` or `f/run` structure.
- Stateful resources have clear disposal or `:managed` lifecycle.
- Reactive values use `:watch` where appropriate instead of manual refresh glue.
- Keys are present for changing sibling widget lists.
- Tests cover pure logic and important widgets.
- Commands in docs/scripts match the project aliases.

## Refactoring guidance

When refactoring:

- Avoid converting idiomatic ClojureDart widget threading into verbose nested Dart-style constructor code unless clarity genuinely improves.
- Separate pure domain logic from Flutter widgets.
- Prefer small composable widget functions returning widgets.
- Keep Dart interop at edges where possible.
- Introduce type hints only where they clarify interop or fix inference issues.
- Preserve hot-reload friendliness: keep `f/run` and avoid unnecessary global side effects.

## Output patterns

### New app

Provide:

1. `deps.edn`.
2. `src/<app>/main.cljd`.
3. Commands to initialize and run.
4. Notes about replacing `<clojuredart-sha>` or using the project's current pinned SHA.

### Bug fix

Provide:

1. Diagnosis by layer.
2. Exact changed namespace/file.
3. Complete corrected code.
4. Command to verify.

### Explain ClojureDart syntax

Provide:

1. The Dart concept.
2. The ClojureDart spelling.
3. A small example.
4. A common mistake to avoid.

### Test generation

Provide:

1. Test namespace.
2. Any required imports.
3. Pure or widget test code.
4. Command with tags or aliases.

## Local reference files in this skill

- `references/canonical-commands.md`
- `references/interop-idioms.md`
- `references/debugging-checklist.md`
- `examples/prompt-examples.md`

Read these when the task is larger than a quick syntax answer.
