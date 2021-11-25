import os
import numpy as np
from utils.common import bcolors
import utils.config as cfg
import timeit





def draw(chessboard,sign = ['--','|','o','x'],pieces_color={}):
    numofsign = len(chessboard[0])*2 + 1

    for i in range(numofsign):
        if(i&1 == 0):
            # print(i&1,'\n')
            print(f"{sign[0]}"*numofsign)
        else:
            str = ''
            for j in range(numofsign):
                if(j&1 == 0 or j==numofsign-1):
                    str += sign[1]
                    # print(sign[0])
                    continue
                pos_sign = chessboard[int(i/2)][int(j/2)]
                if pos_sign != 0:
                    str += ' '
                    has_color = pieces_color.get(1 if pos_sign==1 else 2)
                    str += '' if has_color == None else has_color
                    str += sign[2] if pos_sign==1 else sign[3]
                    str += bcolors.ENDC
                    str += ' '
                    # print(sign[1] if pos_sign==1 else sign[2])
                else:
                    str += '   '
                    # print(' ')
            print(str)


class board():
    def __init__(self,length,vectory_condition=3,pieces_color=None):
        self.length = length
        #双方棋子颜色
        if pieces_color is None:
            self.pieces_color = {
                1: bcolors.RED,
                2: bcolors.BLUE
            }
        else:
            self.pieces_color = pieces_color

        #当前进行玩家
        self.curplayer = 0
        self.curlocation =[]

        #确定几颗棋子能够获胜
        self.vectory_condition = vectory_condition
        #result结果，0为player1胜，1为player2胜，2为平局，3为未分出胜负
        self.winner = 3
        #当前局面,分为两方，甲方与乙方,放入为元组值
        self.aspect1_player = []
        self.aspect2_player = []

        #棋盘显示设定
        self.display = ['--', '|', 'O', 'X']

        #总走棋数
        self.total_chess = 0

        #是否渲染画面
        self.hasrender = 0

        #棋盘数组，用于更新
        self.__chessboard = []
        self._create_board()

    #是否渲染画面
    def render(self,display):
        self.hasrender = display

    #创建棋局，绘制初始局面
    def _create_board(self):
        self.__chessboard = np.zeros((self.length,self.length))
        if self.hasrender:
            draw(self.chessboard,self.display,pieces_color=self.pieces_color)

    #判断当前棋局是否合法，下子的个数，当前玩家对应颜色等是否对应
    def judge_belegal(self,player):
        residual = len(self.aspect1_player) - len(self.aspect2_player)
        if(abs(residual)>1):
            print("__chessboard status is'n legitimate,error that residual greater than 1")
            return False
        if player != self.curplayer:
            print("not match for player role")
            return False
        return True

    #判断当前局面是否得出胜负
    def __judge_status(self):
        #两种思路：1、扫描四条线，从当前棋子节点外的第5颗棋子开始扫描，当遇到无子，异子存储变量置零，达到vectory_condition游戏介绍，定长
        # 2、从当前节点进行回溯深度优先搜索，变长随局面增大而增大
        player_list = [1,2]
        num_of_vectory = self.vectory_condition
        min_loc = min(self.curlocation[0],self.curlocation[1])
        margin_90 = [self.curlocation[0]-num_of_vectory if self.curlocation[1]>=num_of_vectory else 0,self.curlocation[1]]
        margin_135 = [self.curlocation[0]-num_of_vectory,self.curlocation[1]-num_of_vectory] \
            if (self.curlocation[1]>=num_of_vectory and self.curlocation[1]>=num_of_vectory) else [self.curlocation[0]-min_loc,self.curlocation[1]-min_loc]
        margin_180 = [self.curlocation[0],self.curlocation[1]-num_of_vectory if self.curlocation[1]>=num_of_vectory else 0]
        min_loc = min(self.length-self.curlocation[0]-1,self.curlocation[1])
        margin_225 = [self.curlocation[0]+num_of_vectory,self.curlocation[1]-num_of_vectory] \
            if (self.curlocation[1]>=num_of_vectory and self.length-self.curlocation[0]-1>=num_of_vectory) \
            else [self.curlocation[0]+min_loc,self.curlocation[1]-min_loc]
        print(margin_90,margin_135,margin_180,margin_225)

        #四边同时扫
        score = [0,0,0,0]
        curloc_x,curloc_y = 0,0
        for i in range(self.vectory_condition*2):
            curloc_x = i+margin_90[0]
            curloc_y = margin_90[1]
            if(curloc_x<0 or curloc_x>self.length-1): break;
            if(self.__chessboard[curloc_x][curloc_y] not in player_list) or (self.__chessboard[curloc_x][curloc_y] != self.curplayer+1):
                score[0] = 0
            else:
                score[0] = score[0]+1
            if score[0] >= self.vectory_condition: return True
        for i in range(self.vectory_condition*2):
            curloc_x = i+margin_135[0]
            curloc_y = i+margin_135[1]
            if(curloc_x<0 or curloc_x>self.length-1) or (curloc_y<0 or curloc_y>self.length-1): break;
            if(self.__chessboard[curloc_x][curloc_y] not in player_list) or (self.__chessboard[curloc_x][curloc_y] != self.curplayer+1):
                score[1] = 0
            else:
                score[1] = score[1]+1
            if score[1] >= self.vectory_condition: return True
        for i in range(self.vectory_condition*2):
            curloc_x = margin_180[0]
            curloc_y = i+margin_180[1]
            if(curloc_y<0 or curloc_y>self.length-1): break;
            if(self.__chessboard[curloc_x][curloc_y] not in player_list) or (self.__chessboard[curloc_x][curloc_y] != self.curplayer+1):
                score[2] = 0
            else:
                score[2] = score[2]+1
            if score[2] >= self.vectory_condition: return True
        for i in range(self.vectory_condition*2):
            curloc_x = margin_90[0]-i
            curloc_y = margin_90[1]+i
            if(curloc_x<0 or curloc_x>self.length-1) or (curloc_y<0 or curloc_y>self.length-1): break;
            if(self.__chessboard[curloc_x][curloc_y] not in player_list) or (self.__chessboard[curloc_x][curloc_y] != self.curplayer+1):
                score[3] = 0
            else:
                score[3] = score[3]+1
            if score[3] >= self.vectory_condition: return True

        return False


    #进行一步下棋,玩家应遵循0,1,0,1顺序
    def down_chess(self,player,location):
        assert (player < 2),"please place [1,2] chess,this game is subject to biplayer"

        #检测位置边界
        validate_margin = self.__validate_piece(location)
        assert validate_margin,"chess beyond the margin or existed"

        validate_role = self.judge_belegal(player)
        assert validate_role,"not match for player role"

        #绘制 棋盘{0表示空位，1表示玩家1，2表示玩家2}，player则由0,1表示
        self.__chessboard[location[0],location[1]] = player+1
        if self.hasrender:
            draw(self.__chessboard,self.display,pieces_color=self.pieces_color)
        self.curlocation = location
        # print(self.curplayer)

        #记录当前状态
        if not player: self.aspect1_player.append(location)
        else: self.aspect2_player.append(location)
        self.total_chess += 1
        #判断胜负
        vectory = self.__judge_status()
        if vectory == True:
            self.winner = player
            print(f"player {self.curplayer} is vectory")
        if self.total_chess >= (self.length**2) and (self.winner == 3):
            self.winner = 2
        self.curplayer = self.curplayer^1


    #验证棋子的有效性
    def __validate_piece(self,location):
        margin = self.length
        print(bcolors.HEADER + f"{location}" + bcolors.ENDC)
        if location[0]<0 or location[1]<0:
            return False
        if location[0]>margin-1 or location[1]>margin-1:
            return False
        if self.__chessboard[location[0]][location[1]]:
            return False
        return True

    #hash函数，对当前状态进行简化
    def hash(self):
        #padding棋盘
        board = self.__chessboard
        pad = int((cfg.MAX_LEN - self.length) / 2)

        if self.length%2 == 0:
            board = np.pad(board, ((pad, pad), (pad, pad)), 'constant')
        else:
            board = np.pad(board, ((pad+1, pad), (pad, pad+1)), 'constant')



#障碍生成器，主要用来描述变化情况下的局面环境，
# 在局面中随机载入障碍点，此类点不可存在棋子,增加算法泛化能力
class ObstacleGenerator():
    def __init__(self):
        pass



if __name__ == "__main__":
    mat = np.zeros((32,32))
    mat[1,3] = 1
    mat[2,5] = 2

    pieces_color = {
        1: bcolors.RED,
        2: bcolors.BLUE
    }
    # draw(mat,pieces_color=pieces_color)

    chsboard = board(5,4)
    # chsboard.__chessboard = np.random.randint(0,3,(5,5))
    # chsboard.__chessboard = np.array([[1,0,0,0,0],[0,0,0,0,2],[0,2,1,0,0],[0,0,2,0,1],[0,0,2,0,0]])
    # chsboard.render(1)
    chsboard.down_chess(0,[1,1])
    chsboard.hash()

    # chsboard.down_chess(1, [3, 4])
    # print(mat)

