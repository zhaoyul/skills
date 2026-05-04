# Prompt examples for the ClojureDart Skill

## Create an app

> Create a minimal ClojureDart Flutter app with a counter, using `cljd.flutter`, and give me the full `deps.edn` and `src/acme/main.cljd`.

## Convert Dart Flutter code

> Convert this Dart Flutter widget into idiomatic ClojureDart. Preserve named arguments, static properties, and widget composition style.

## Debug a build error

> This command fails: `clj -M:cljd flutter`. Diagnose which layer is failing and give me the smallest fix. Here is the output: ...

## Review code

> Review this `.cljd` namespace for ClojureDart idioms, Flutter lifecycle problems, bad interop syntax, and hot-reload issues. Return a corrected full namespace.

## Add tests

> Add `cljd.test` tests for this namespace. Include pure logic tests and one widget test tagged `:widget` if appropriate.

## Explain syntax

> Explain how Dart named arguments, constructors, static properties, object fields, nullable type hints, and generics are written in ClojureDart, with examples.
