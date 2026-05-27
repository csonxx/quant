# Lab 02 数据偏差检查

## 目标

学会先怀疑数据。

## 命令

```bash
python3 -m unittest tests.test_data
```

## 练习

1. 复制 `data/samples/ohlcv_demo.csv` 到临时文件。
2. 删除 `close` 列，看加载器是否报错。
3. 把某天 `high` 改得小于 `open`，看加载器是否报错。
4. 把某天价格改成负数，解释为什么这会污染收益。

## 答案方向

数据契约越早失败越好。错误数据进入模型后，定位成本会指数级上升。
