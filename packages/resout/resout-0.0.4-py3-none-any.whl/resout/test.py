
# 画像等の結果出力パス管理 [resout]
# 【動作確認 / 使用例】

import sys
import numpy as np
from ezpip import load_develop
resout = load_develop("resout", "../", develop_flag = True)

# 保存パスの設定 [resout]
resout.set_save_dir("./results/")

for _ in range(2):
	# 保存ファイル名の生成(自動で連番になる) [resout]
	filename = resout.gen_save_path(".txt", label = "exp_result")
	print(filename)
	with open(filename, "w", encoding = "utf-8") as f:
		f.write("hoge")

img = np.zeros((200,200,3), dtype = np.uint8)
# 画像の保存 [resout]
resout.save_img(img, ratio = 1.0, ext = ".png", label = "resout_img", interpolation = "INTER_CUBIC")
