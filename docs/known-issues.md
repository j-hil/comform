# Known Issues

## Missing Edge Cases

These are cases that I knowingly haven't for. I'll add them as and when they actually
arise during my use.

- long headers
- sequential block comments differently aligned, eg:

```python
for x in y:
    pass
    # in loop comment
# out loop comment
```
