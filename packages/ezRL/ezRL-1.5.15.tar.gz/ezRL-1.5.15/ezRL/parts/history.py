
# 棋譜関係処理 [history.py]

import os
import sys
import json
import resout as rout

# 棋譜をjson形式で保存 [history.py]
def save_history_json(history_ls, filename):
	# stepごとに改行区切りしたjsonの作成
	step_ls = [
		"  " + json.dumps(step, ensure_ascii = False)
		for step in history_ls]
	comma_ls = ",\n".join(step_ls)
	json_str = "[\n%s\n]"%comma_ls
	# 保存ファイル名の生成(自動で連番になる) [resout]
	with open(filename, "w", encoding = "utf-8") as f:
		f.write(json_str)

# 保存先フォルダ作成
def make_save_dir(history_filename):
	ext = ".json"
	if history_filename[-len(ext):] != ext:
		raise Exception("[ezRL error] history_filenameは拡張子が「%s」であることが想定されています"%ext)
	save_dir = "%s/"%(history_filename[:-len(ext)])
	if os.path.exists(save_dir) is True:
		raise Exception("[ezRL error] 保存先フォルダがすでに存在します")
	os.mkdir(save_dir)
	return save_dir

# 棋譜の画像化 (デフォルトは入力棋譜と同じディレクトリに置かれる)
def history2img(
	history_filename,	# 棋譜ファイル名
	game,	# ゲーム
	output_file_flag = True,	# ファイル出力フラグ
	file_out_ratio = 1.0
):
	# 棋譜ファイル読み込み
	with open(history_filename, "r", encoding = "utf-8") as f:
		history_ls = json.load(f)
	# 画像化
	img_ls = []
	for step in history_ls:
		state = step["state"]
		img = game.human_obs(state)
		img_ls.append(img)
	# ファイル出力フラグ判断
	if output_file_flag is True:
		# 保存先フォルダ作成
		save_dir = make_save_dir(history_filename)
		# 画像ファイル出力
		for idx, img in enumerate(img_ls):
			img_filename = "%s/%d.png"%(save_dir, idx)
			rout._raw_save_img(img, img_filename, ratio = file_out_ratio)	# pltを使ったcv2形式の画像保存
	return img_ls
