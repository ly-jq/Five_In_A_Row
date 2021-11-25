from gym import spaces, core


# core.Env是gym的环境基类,自定义的环境就是根据自己的需要重写其中的方法；
# 必须要重写的方法有:
# __init__()：构造函数
# reset()：初始化环境
# step()：环境动作,即环境对agent的反馈
# render()：如果要进行可视化则实现

class MyEnv(core.Env):
    def __init__(self):
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,))  # 动作空间
        self.observation_space = spaces.Box(low=-1, high=1, shape=(1,))  # 状态空间

    # 其他成员

    def reset(self):
        ...
        obs = self.get_observation()
        return obs

    def step(self, action):
        ...
        reward = self._get_reward()
        done = self._get_done()
        obs = self._get_observation(action)
        info = {}  # 用于记录训练过程中的环境信息,便于观察训练状态
        return obs, reward, done, info

    # 根据需要设计相关辅助函数
    def _get_observation(self, action):
        obs = action
        return obs


    def _get_reward(self):
        reward = 1
        return reward

    def _get_done(self):
        done = 0
        return done
