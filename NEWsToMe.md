# NEWs to me in this book

```python
indonesia_quakes = quakes.query("parsed_place == 'Indonesia'").assign(
    time=lambda x: pd.to_datetime(x["time"], unit='ms'),
    earthquake=1
).set_index("time").resample("1D").sum()
```

`assign` 配合 `lambda` 使用，可以减少中间很多行，将代码写成块。
