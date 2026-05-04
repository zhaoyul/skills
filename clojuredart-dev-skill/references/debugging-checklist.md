# ClojureDart debugging checklist

## Before changing code

- What exact command failed?
- Which layer produced the error: Clojure CLI, ClojureDart compiler, Dart, Flutter, runtime, or tests?
- What changed since the last successful run?
- Are `deps.edn`, `pubspec.yaml`, and `:cljd/opts` aligned?
- Does the `:main` namespace exist and define `(defn main [] ...)`?

## Common symptoms

### Dart package symbol cannot be resolved

Check namespace require syntax:

```clojure
(:require ["package:flutter/material.dart" :as m])
```

Check `pubspec.yaml` for non-SDK packages.

### Named argument mismatch

Dart `foo: value` becomes `.foo value`.

### Constructor mismatch

ClojureDart uses `(Type args...)`, not `(new Type ...)` or `(Type. ...)`.

### Flutter did not update

- Confirm watcher compiled successfully.
- Press return in the watcher to restart.
- Try `clj -M:cljd clean` if generated state is stale.

### Device not selected

```sh
flutter devices
clj -M:cljd flutter -d <device-id>
```

### Widget list state jumps around

Check for stable keys on changing sibling widgets. Prefer `:key` in `f/widget` where it fits.

### Resource leak or controller lifecycle bug

Look for controllers, animations, focus nodes, streams, and listenables. Consider `:managed` and explicit dispose behavior.
