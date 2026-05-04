# Code Speech Style Guide

This reference defines how to read code in technical audiobooks.

## General pattern

1. Identify language and purpose.
2. State control flow and data flow.
3. Read exact syntax only when it teaches something or prevents ambiguity.
4. Put long exact readings in the detail track.

## Length policy

| Code length | Main track policy |
|---|---|
| 1 to 5 lines | Semantic reading plus exact compact reading if useful. |
| 6 to 20 lines | Summarize structure, then read key lines. |
| 20+ lines | Explain architecture, functions, branches, invariants. Avoid line-by-line reading. |
| Configuration files | Read key fields and values, not every brace and quote. |
| Regex, macros, pointer tricks | Use exact or token mode for the critical fragment. |

## Operator rules

| Token | Preferred reading |
|---|---|
| `=` | `赋值` |
| `==` | `双等号, 相等比较` |
| `===` | `三等号, 严格相等` |
| `!=` | `不等于` |
| `!==` | `严格不等于` |
| `<` | `小于` |
| `<=` | `小于等于` |
| `>` | `大于` |
| `>=` | `大于等于` |
| `&&` | `逻辑与` |
| `||` | `逻辑或` |
| `!` | `逻辑非`, or `null-forgiving` in C# if context requires |
| `&` | `按位与`, `取地址`, or `引用标记`, depending on language/context |
| `|` | `按位或`, `管道`, or `union`, depending on language/context |
| `^` | `按位异或` in code, not exponent |
| `~` | `按位取反` |
| `+=` | `加等于` |
| `++` | `自增` |
| `--` | `自减` |
| `->` | `箭头`, or `通过指针访问` in C/C++ |
| `=>` | `lambda 箭头` |
| `::` | `双冒号` |
| `? :` | `三元条件表达式` |

## C examples

Source:

```c
int *p = &x;
```

Main track:

```text
声明一个指向 int 的指针 p, 并让它保存 x 的地址.
```

Detail track:

```text
int 星 p 赋值 ampersand x. 这里星号表示指针声明, ampersand 表示取地址.
```

Source:

```c
sum += a[i];
```

Reading:

```text
sum 加等于 a 方括号 i.
```

## Java examples

Source:

```java
Map<String, List<Integer>> index = new HashMap<>();
```

Main track:

```text
声明一个 index, 类型是 Map, key 是 String, value 是 Integer 列表. 初始化为新的 HashMap.
```

Detail track:

```text
Map of String to List of Integer, index 赋值 new HashMap.
```

Avoid reading every angle bracket unless the section teaches generic syntax.

## C# examples

Source:

```csharp
public async Task<User?> GetUserAsync(Guid id)
```

Main track:

```text
声明一个 public async 方法 GetUserAsync. 它返回 Task of nullable User, 参数是 Guid id.
```

Source:

```csharp
users.Where(u => u.IsActive)
```

Reading:

```text
users dot Where, lambda u, 条件是 u dot IsActive.
```

For C# nullable annotations:

| Syntax | Reading |
|---|---|
| `User?` | `nullable User` |
| `name!` | `name 后面的感叹号表示 null-forgiving` |
| `x?.Name` | `x null 条件访问 Name` |
| `x ?? fallback` | `x null 合并 fallback` |

## Lisp, Scheme, and Clojure examples

Source:

```lisp
(define (square x)
  (* x x))
```

Main track:

```text
定义函数 square, 参数 x, 返回 x 乘 x.
```

Detail track:

```text
define 一个函数形式, 函数名 square, 参数 x. 函数体是乘法表达式 x x.
```

Do not read every parenthesis in the main track.

## API chains

Source:

```csharp
users.Where(u => u.IsActive)
     .OrderByDescending(u => u.CreatedAt)
     .Take(10)
```

Main track:

```text
这条调用链先筛选活跃用户, 再按 CreatedAt 降序排序, 最后取前 10 个.
```

Detail track:

```text
users dot Where, lambda u, 条件是 u dot IsActive. 接着 dot OrderByDescending, lambda u, key 是 u dot CreatedAt. 最后 dot Take 10.
```

## Safety against hallucination

If code is incomplete or depends on missing context, do not pretend to know everything. Use wording like:

```text
从这个片段可以确定的是...
```

or:

```text
如果 compare 函数遵循常见约定, 这里会按升序排序. 但片段本身没有给出 compare 的定义.
```
