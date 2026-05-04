# Math Speech Style Guide

This reference defines how to read LaTeX formulas in technical audiobooks.

## General pattern

1. Name the formula or state its purpose.
2. Read the outer structure first.
3. Only then read inner terms.
4. Move long exact readings to the detail track.

Example:

```latex
p_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}
```

Main track:

```text
这是 softmax 的定义. p 下标 i 等于 e 的 z 下标 i 次方, 除以所有类别上的指数和.
```

Detail track:

```text
p 下标 i 等于一个分式. 分子是 e 的 z 下标 i 次方. 分母是对 j 从 1 到 K 求和, e 的 z 下标 j 次方.
```

## Symbol rules

| LaTeX | Preferred reading | Notes |
|---|---|---|
| `x_i` | `x 下标 i` | Use `sub i` if the narration is mostly English. |
| `x^2` | `x 平方` | For general exponent: `x 的 k 次方`. |
| `x_i^2` | `x 下标 i 的平方` | Avoid confusion with `x_{i^2}`. |
| `x_{i^2}` | `x 下标 i 平方` | Spell scope if ambiguity matters. |
| `\frac{a+b}{c-d}` | `分式, 分子 a 加 b, 分母 c 减 d` | Prefer explicit numerator/denominator. |
| `\sqrt{x+1}` | `x 加 1 的平方根` | For short cases, `根号 x 加 1` is acceptable. |
| `\sum_{i=1}^{n} a_i` | `对 i 从 1 到 n 求和 a 下标 i` | Include limits. |
| `\prod_{i=1}^{n} a_i` | `对 i 从 1 到 n 连乘 a 下标 i` | Include limits. |
| `\int_0^1 f(x)\,dx` | `从 0 到 1 对 x 积分 f of x` | Include integration variable. |
| `\partial f / \partial x` | `f 关于 x 的偏导数` | Use semantic reading. |
| `\nabla_\theta L` | `L 关于 theta 的梯度` | Avoid only saying `nabla`. |
| `O(n \log n)` | `大 O, n log n` | For complexity, no need to read parentheses every time. |
| `p(y \mid x)` | `p of y given x` or `y 在给定 x 条件下的概率` | Avoid `vertical bar`. |
| `A \in \mathbb{R}^{m \times n}` | `A 属于 m 乘 n 维实数矩阵空间` | Semantic reading is clearer. |
| `\arg\max_x f(x)` | `使 f of x 最大的 x` | Use semantic reading in main track. |
| `\lambda x. x` | `lambda x, 返回 x` | In programming contexts, explain as function. |

## Fractions

Prefer:

```text
分式, 分子..., 分母...
```

Use `over` only for very short expressions:

```text
a over b
```

Do not read:

```text
a plus b over c minus d
```

unless the grouping is already obvious from context.

## Functions and probabilities

Read function application compactly:

```text
f of x
```

For Chinese-heavy narration, use:

```text
f 作用于 x
```

For conditional probability:

```latex
p_\theta(y_i \mid x_i)
```

Preferred:

```text
p 下标 theta, y 下标 i given x 下标 i
```

or:

```text
模型参数 theta 下, 给定 x 下标 i 时 y 下标 i 的概率
```

## Derivations and aligned equations

For multi-line derivations:

1. Main track summarizes the purpose and the transformation.
2. Read only the first and final equations unless the intermediate steps matter.
3. Detail track may read each line precisely.

Example main track:

```text
接下来的三行把对数似然的乘积形式改写成求和形式. 关键变化是利用 log of product 等于 sum of logs.
```

## Matrices and tensors

Main track should usually say what the object is:

```text
这里的 X 是一个 n by d 的设计矩阵, 每一行对应一个样本.
```

Detail track can read dimensions and selected entries. Avoid reading every matrix entry unless the matrix is small and important.

## LaTeX verbatim mode

Use verbatim LaTeX reading only for LaTeX teaching, macro definitions, or source-level comparison.

Example:

```latex
\newcommand{\R}{\mathbb{R}}
```

Verbatim reading:

```text
反斜杠 newcommand, 左花括号反斜杠 R 右花括号, 左花括号反斜杠 mathbb 左花括号 R 右花括号右花括号.
```
