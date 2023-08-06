# resout

This description is under construction.

## 概要
Output path management tool for results (images, etc.) of numerical experiments, etc.
数値実験等の結果(画像等)の出力パス管理ツール

## 基本的な使い方
```python
import resout

# 保存ファイル名の生成(自動で連番になる) [resout]
filename = resout.gen_save_path(".txt", label = "exp_result")
with open(filename, "w", encoding = "utf-8") as f:
	f.write("hoge")
```

上記のように、`gen_save_path()`関数を使用することで連番のファイル名を取得できる

## 連番の説明
```python
import resout

print(resout.gen_save_path(".txt", "exp_result"))	# -> <path>\output_img\20210605T144210\exp_result_0.txt
print(resout.gen_save_path(".txt", "exp_result"))	# -> <path>\output_img\20210605T144210\exp_result_1.txt
print(resout.gen_save_path(".txt", "exp_result"))	# -> <path>\output_img\20210605T144210\exp_result_2.txt
```

## 画像を保存する
```python
import resout
import numpy as np

img = np.zeros((200,200,3), dtype = np.uint8)
# 画像の保存 [resout]
resout.save_img(img, ratio = 1.0, ext = ".png", label = "resout_img")
```

## 保存パスの変更
```python
import resout

# 保存パスの設定 [resout]
resout.set_save_dir("./results/")

# 保存ファイル名の生成(自動で連番になる) [resout]
filename = resout.gen_save_path(".txt", label = "exp_result")
with open(filename, "w", encoding = "utf-8") as f:
	f.write("hoge")
```
