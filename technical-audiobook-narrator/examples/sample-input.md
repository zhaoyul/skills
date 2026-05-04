# Sample input

Now we define the cross entropy loss:

```math id=eq-cross-entropy
L(\theta) = -\sum_{i=1}^{n} y_i \log p_\theta(y_i \mid x_i)
```

The following loop computes the sum of an array prefix:

```c id=listing-for-sum
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += a[i];
}
```
