import sys
sys.path.append('./BoardEnv')
import gym
import BoardEnv

env = gym.make('env_name-v0') # 参数为环境的id

obs = env.reset()

for i in range(1000):
	action = 1
	obs, reward, done, info = env.step(action)
	if done:
		break