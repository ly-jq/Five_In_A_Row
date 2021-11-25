import numpy as np
import BoardDesign
import utils.config as cfg

#采用自博弈思想，每次比赛与之前部分最佳的policy进行博弈


#真实玩家
class RobiticPlayer():
    def __init__(self):
        # 经验回访容器
        self.status_buff = []
        self.reward_buff = []
        self.action_buff = []


    #重设经验
    def reset(self):
        self.status_buff.clear()
        self.reward_buff.clear()
        self.action_buff.clear()

    #执行一次行动 前向传播后，进行概率探索返回回报
    def act(self):
        pass

    def update(self):
        pass
    #每次行动进行状态记录
    def set_status(self):
        pass

    #行动后对

#电脑玩家
class Player(RobiticPlayer):
    def __init__(self):
        super(RobiticPlayer,self).__init__()
        pass

class judger():
    def __init__(self):
        pass
