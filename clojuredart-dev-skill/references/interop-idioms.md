# ClojureDart interop idioms

## Dart imports

```clojure
(ns my.project
  (:require ["package:flutter/material.dart" :as m]
            [cljd.flutter :as f]))
```

## Constructors

```clojure
(StringBuffer "hello")
(m/Text "Hello")
(List/empty .growable true)
```

## Named arguments

```clojure
(m/Text "Hello world"
  .maxLines 2
  .softWrap true
  .overflow m/TextOverflow.fade)
```

## Static properties and enum values

```clojure
m/Colors.purple
m/Colors.purple.shade900
m/TextAlign.left
```

## Instance properties

```clojure
(.-height size)
(.-value! controller "new value")
(set! (.-value controller) "new value")
```

## Object destructuring

```clojure
(let [{:flds [height width]} size]
  ...)
```

## Nullability hints

```clojure
^String   ; non-null
^String?  ; nullable
```

## Generic type hints

```clojure
^#/(List Map) x
```

## `cljd.flutter` widget threading

```clojure
(f/widget
  m/MaterialApp
  .home
  m/Scaffold
  .body
  m/Center
  (m/Text "Hello"))
```

## Reactive widget body

```clojure
(f/widget
  :watch [v an-atom]
  (m/Text (str v)))
```
