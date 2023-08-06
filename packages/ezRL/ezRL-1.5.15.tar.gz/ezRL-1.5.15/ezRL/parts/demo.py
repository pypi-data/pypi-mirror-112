
# デモ [demo.py]

import sys
# 複数エピソード実行
from .episode import do_episodes

# デモ (DQN-catcher) [demo.py]
def dqn_catcher_demo():
	import resout as rout
	from relpath import add_import_path
	add_import_path("./")
	import catcher_game as game	# Catcherゲーム [catcher_game]
	from DQN_Agent import DQN_Agent	# Deep Q Network AI [DQN_Agent]
	rout.set_save_dir("./ezRL_demo_output/")	# 保存パスの設定 [resout]
	train_ai = DQN_Agent(action_ls = game.action_ls, ai_obs = game.ai_obs) # Deep Q Network AI
	do_episodes(game, train_ai, game_params = {}, episode_n = 700, save_reward_ls = True)	# 複数エピソード実行
	test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
	do_episodes(game, test_ai, game_params = {}, episode_n = 1, save_history = True)	# 複数エピソード実行
	print("demo finished! (results are in \"./ezRL_demo_output/\".)")

# デモ (Random-catcher) [demo.py]
def random_catcher_demo():
	import resout as rout
	import catcher_game as game	# Catcherゲーム [catcher_game]
	from .debug_players import RandomPlayer	# ランダムAI
	rout.set_save_dir("./ezRL_demo_output/")	# 保存パスの設定 [resout]
	train_ai = RandomPlayer(action_ls = game.action_ls, ai_obs = game.ai_obs)	# ランダムAI
	do_episodes(game, train_ai, game_params = {}, episode_n = 30, save_reward_ls = True)	# 複数エピソード実行
	test_ai = train_ai.gen_test()	# テスト用プレーヤーを生成 [DQN_Agent]
	do_episodes(game, test_ai, game_params = {}, episode_n = 5, save_history = True)	# 複数エピソード実行
	print("demo finished! (results are in \"./ezRL_demo_output/\".)")

# デモ [demo.py]
def demo(demo_name = "DQN-catcher"):
	if demo_name == "DQN-catcher":
		dqn_catcher_demo()	# デモ (DQN-catcher) [demo.py]
	elif demo_name == "Random-catcher":
		random_catcher_demo()	# デモ (Random-catcher) [demo.py]
	else:
		raise Exception("[ezRL error] invalid demo name.")
