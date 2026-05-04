# ClojureDart canonical commands

```sh
clj -M:cljd init
clj -M:cljd flutter
clj -M:cljd compile
clj -M:cljd clean
clj -M:cljd upgrade
clj -M:cljd test
```

## Typical workflows

### Create and run a Flutter app

```sh
clj -M:cljd init
clj -M:cljd flutter
```

### Run on a specific device

```sh
flutter devices
clj -M:cljd flutter -d <device-id>
```

### Run tests

```sh
clj -M:cljd test
clj -M:cljd test ns.to.test1 ns.to.test2
clj -M:cljd test -- -t widget
clj -M:test:cljd test
```

### Clean stale state

```sh
clj -M:cljd clean
```

### Update ClojureDart dependency

```sh
clj -M:cljd upgrade
```

## Troubleshooting note

Classify failures into one of these layers before suggesting a fix:

1. Clojure CLI / tools.deps / git dependency.
2. ClojureDart compiler.
3. Dart package / pubspec.
4. Flutter device/platform tooling.
5. Runtime widget/state behavior.
6. Test runner / tags / integration test directory.
