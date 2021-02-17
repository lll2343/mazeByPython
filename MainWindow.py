"""
---------------------------
@author：刘羊周 息睿 黄健鹏
---
2020年度python课程期末考核设计

2281250383@qq.com
---------------------------
"""

"""
迷宫算法： 生成与求解
 迷宫生成
   DFS（深度优先）递归与非递归
   十字分割算法生成 递归
   随机prim算法 非递归 
 迷宫求解
  DFS

一些说明
    迷宫大小为31*31(可以不固定，但用奇数）
    最外围为墙，入口坐标（0,1）出口坐标（N-1，N-2)
    最外围是墙或者入口，对迷宫的操作范围为（1,1）,(N-2,N-2)
"""


from tkinter import *
import time
from enum import Enum
import random
from typing import Deque


# 迷宫大小（奇数）
# 调试的时候可以用小一点的，记住是奇数
MazeSIZE = 31

# 延时
Delay = 0.01

# 矩形大小 路或者是墙 小方格的大小
RecSIZE = 15

# 四个方向
Dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]


# 二维点
class Point2(object):
    def __init__(self, _x=0, _y=0):
        self.x = _x
        self.y = _y

    def equal(self, another):
        return self.x == another.x and self.y == another.y
    
    # 输出坐标点
    def showSeat(self):
        print(self.x,self.y,end="\t")


# 枚举迷宫方格状态
class CellState(Enum):
    PATH = int(0)
    WALL = int(1)
    FLAG = int(2)

# 用于窗口的跳转
class BaseDesk(object):
    def __init__(self, master):
        self.window = master
        self.window.config()
        self.window.configure(bg="white")
        # 设置窗口固定不可改变大小
        self.window.resizable(0, 0)
        self.window.title("迷宫生成与求解演示")
        self.window.geometry('495x520')
        MazeGraph(self.window)


# 主窗口类
class MazeGraph(object):
    def __init__(self, master):
        self.window = master
        self.menu = Frame(self.window, height=495, width=520)
        self.menu.pack()
        label1 = Label(self.menu, width=50, height=4, text='迷宫的生成和求解图形化演示',
                       font=("Courier", 21, "bold"), fg='red')
        label1.pack()
        textList = ["1. DFS生成 + DFS寻路",
                    "2. DFS生成 + 随机方向DFS寻路",
                    "3. 分割生成 + DFS寻路",
                    "4. 分割生成 + 随机方向DFS寻路",
                    "5. Prim生成 + DFS寻路",
                    "6. Prim生成 + 随机方向DFS寻路"]

        # 使用pack布局
        for inx, cmd in enumerate(textList):
            Button(self.menu, anchor='w', width=30, height=2,
                   relief='flat', overrelief='groove', text=cmd,
                   font=("Courier", 14, "bold"),
                   command=lambda arg=inx: self.clickBtn(arg)).pack(expand=True)

        self.btn_quit = Button(self.menu, text='退出', width=10,
                               height=1, command=quit)
        self.btn_quit.pack(anchor='se')

    def clickBtn(self, index):
        self.menu.destroy()
        # 在这里还需要一个参数，然后在MazeShow里面的init进行判断，选择生成算法和求解算法
        MazeShow(self.window, index)
        # print('index' + str(index))


# 迷宫求解展示界面
class MazeShow(object):
    def __init__(self, master, index):
        # 界面部分
        self.window = master
        self.face = Frame(self.window, bg='white')
        self.face.pack()
        self.canvas = Canvas(self.face, width=495, height=480, bg='white')
        # print(self.canvas.size)
        self.canvas.create_rectangle(15, 15, 480, 480)
        self.canvas.pack()
        self.btn_back = Button(self.face, width=10, height=1,
                               text='返回', command=self.back)

        # 一些画图的属性，矩形大小，延时
        self.delayTime = Delay
        self.recSize = RecSIZE

        # 迷宫部分
        self.size = MazeSIZE
        self.map = [[CellState.WALL] * self.size for i in range(self.size)]
        self.start = Point2(1, 0)
        self.end = Point2(self.size - 2, self.size - 1)

        # 初始化迷宫的画布
        self.InitGame()

        # 此处对应每一个按钮执行不同的操作
        if index == 0:
            # DFS生成 + DFS寻路
            # DFS递归生成迷宫
            x = random.randrange(1, self.size - 1, 2)
            y = random.randrange(1, self.size - 1, 2)
            self.DFSGenerator(x, y)
            # DFS寻路，非递归
            result = self.DFSFind()
            
            # 输出DFS路径
            # for seat in result:
            #    seat.showSeat()

        elif index == 1:
            # DFS生成 + 随机方向DFS寻路
            # DFS递归生成迷宫
            x = random.randrange(1, self.size - 1, 2)
            y = random.randrange(1, self.size - 1, 2)
            self.DFSGenerator(x, y)
            # 控制台调试
            # self.showAtConsol()
            self.DFSFind(True)

        elif index == 2:
             # 分割生成 + DFS寻路
            self.DivisionGenerate()

            self.DFSFind()

        elif index == 3:
             # 分割生成 + 随机方向DFS寻路
            self.DivisionGenerate()
            # 控制台调试
            # self.showAtConsol()
            self.DFSFind(True)

        elif index == 4:
            # Prim生成 + DFS寻路
            self.PrimGenerator()
            self.DFSFind()
        else:
            # Prim生成 + 随机方向DFS寻路
            self.PrimGenerator()
            # 控制台调试
            # self.showAtConsol()
            self.DFSFind(True)
        
        # 按钮在动画之后再进行展示
        self.btn_back.pack(side='bottom')

    # 返回按钮的实现    
    def back(self):
        self.face.destroy()
        MazeGraph(self.window)

    # 画矩形部分,白色作为路，黑色作为路径
    def DrawRectangle(self, x, y, color="white", delay=True):
        """
        矩形对应位置
        map[i][j]
        15+j*self.recSize 15+i*self.recsize
        15+(j+1)*self.recSize 15+(i+1)*self.recSize
        """
        self.canvas.create_rectangle(15 + y * self.recSize,
                                     15 + x * self.recSize,
                                     15 + (y + 1) * self.recSize,
                                     15 + (x + 1) * self.recSize,
                                     fill=color)
        self.canvas.update()
        if delay:
            time.sleep(self.delayTime)

    # DFS生成(挖墙)
    """
    1.初始时全部是墙
    2.随机选取一个点（奇数）将其挖开，并入栈
    3.四个方向随机选择一个方向，设当前挖开坐标为（x,y)若该方向上
    满足（x+dx*2,y+dy*2)是墙，则挖开，并将新挖开的点入栈
    4.将新挖的作为当前点，重复操作2
    5.若当前点不能继续挖，则pop，并将当前点重置为栈中元素
    6.当栈空时，结束
    """

    # 非递归，迭代版 还有问题！！！！
    def DFSIterativeGenerator(self):
        # 用list定义栈
        sp = []
        # 随机生成一个坐标，要求为奇数
        temp = Point2(random.randrange(1, self.size - 1, 2),
                      random.randrange(1, self.size - 1, 2))
        sp.append(Point2(temp.x, temp.y))
        # 迭代生成并图形展示
        while len(sp) != 0:
            if self.map[temp.x][temp.y] != CellState.PATH:
                self.map[temp.x][temp.y] = CellState.PATH
                # 画矩形
                self.DrawRectangle(temp.x, temp.y)

            # 随机打乱方向
            random.shuffle(Dir)
            index = 0
            while index < 4:
                if 1 <= temp.x + 2 * Dir[index][0] <= self.size - 2 and \
                        1 <= temp.y + 2 * Dir[index][1] <= self.size - 2 and \
                        self.map[temp.x + 2 * Dir[index][0]][temp.y + 2 * Dir[index][1]] == CellState.WALL:
                    self.map[temp.x + Dir[index][0]][temp.y + Dir[index][1]] = CellState.PATH

                    # 画矩形
                    self.DrawRectangle(temp.x + Dir[index][0], temp.y + Dir[index][1])

                    temp.x += 2 * Dir[index][0]
                    temp.y += 2 * Dir[index][1]
                    sp.append(Point2(temp.x, temp.y))
                index += 1
            if index == 4:
                sp.pop()
            if len(sp) != 0:
                temp = sp[-1]

    # 递归DFS生成
    def DFSGenerator(self, x, y):
        # 随机打乱方向
        random.shuffle(Dir)
        self.map[x][y] = CellState.PATH

        # 画矩形
        self.DrawRectangle(x, y)

        index = 0
        # 递归生成迷宫
        while index < 4:
            if 1 <= x + 2 * Dir[index][0] <= self.size - 2 and \
                    1 <= y + 2 * Dir[index][1] <= self.size - 2 and \
                    self.map[x + 2 * Dir[index][0]][y + 2 * Dir[index][1]] == CellState.WALL:
                self.map[x + Dir[index][0]][y + Dir[index][1]] = CellState.PATH

                # 画矩形
                self.DrawRectangle(x + Dir[index][0], y + Dir[index][1])

                self.DFSGenerator(x + 2 * Dir[index][0], y + 2 * Dir[index][1])
            index += 1

    # DFS寻路 非递归方式
    """
    从起点开始，将当前点入栈，向某一方向前进。
    若周围方向均不能继续前进，则回退，
    直到 找到终点 或 栈 为空，就不再贴图
    """
    def DFSFind(self,rand=False):
        # 先往下和右搜路
        direction = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        
        # rand为真，则打乱方向
        if rand:
            random.shuffle(direction)
        
        # 定义的堆栈数据结构
        sp = []
        temp = self.start
        # 开始的时候不需要画路径
        sp.append(Point2(temp.x, temp.y))

        while len(sp) != 0:
            index = 0
            while index < 4:
                if 0 <= temp.x + direction[index][0] <= self.size - 1 and \
                        0 <= temp.y + direction[index][1] <= self.size - 1 and \
                        self.map[temp.x + direction[index][0]][temp.y + direction[index][1]] == CellState.PATH:
                    # 对走过的路进行标记
                    self.map[temp.x][temp.y] = CellState.FLAG

                    self.DrawRectangle(temp.x, temp.y, "blue")

                    temp.x += direction[index][0]
                    temp.y += direction[index][1]
                    sp.append(Point2(temp.x, temp.y))

                    # 画矩形
                    self.DrawRectangle(temp.x, temp.y, "yellow")

                    if temp.equal(self.end):
                        return sp
                    break
                index += 1
            if index == 4:
                self.map[temp.x][temp.y] = CellState.FLAG

                # 画矩形,白色路径
                self.DrawRectangle(temp.x, temp.y, "white")
                # 此处吉老师牛逼啊
                # print(temp.x, temp.y, "green")  #####
                sp.pop()
                if len(sp) != 0:
                    self.DrawRectangle(sp[-1].x, sp[-1].y, "yellow")
                    temp = Point2(sp[-1].x, sp[-1].y)

        # 将被标记的路重新还原
        for iter_1 in self.map:
            for iter_2 in iter_1:
                if iter_2 == CellState.FLAG:
                    iter_2 = CellState.PATH
        return sp

    # 分割 补墙生成 递归版
    """
    1.初始时除了四周全通路
    2.x，y 均在 1~N-2 中随机选取一点（均为偶数），然后十字建墙
    3.在建好的四面墙（不包含选取点）中随机选择三面，
      找奇数点开洞，使得四个子空间连通
    4.对四个子空间重复操作（一个十字的墙将整个迷宫分为了四个小的部分再递归）
      直到子空间不可分割为止（何时不可分割？长度 或 宽度 不大于 1 时）
    """
    def DivisionGenerator(self,_l,_r,_t,_b):
        if _r-_l>1 and _b-_t>1:
            i=0
            # 生成的分割点为偶数
            # _l _r均为奇数
            px = random.randrange(_l+1,_r+1,2)
            py = random.randrange(_t+1,_b+1,2)
            while px+i <= _r or px-i>=_l or py+i<=_b or py-i>=_t:
                if px+i <= _r:
                    self.map[px+i][py] = CellState.WALL
                    self.DrawRectangle(px+i,py,"black")
                if px-i >= _l:
                    self.map[px-i][py] = CellState.WALL
                    self.DrawRectangle(px-i,py,"black")
                if py+i <= _b:
                    self.map[px][py+i] = CellState.WALL
                    self.DrawRectangle(px,py+i,"black")
                if py-i >= _t:
                    self.map[px][py-i] = CellState.WALL
                    self.DrawRectangle(px,py-i,"black")
                i += 1

            # 随机在三面墙上开洞，开洞位置是 奇数
            # l r t b 都是奇数
            # px py 是偶数
            dir = [0,1,2,3]
            random.shuffle(dir)
            for index in range(3):
                if dir[index]==0:
                    xx = random.randrange(_l,px,2)
                    self.map[xx][py] = CellState.PATH
                    self.DrawRectangle(xx,py)
                elif dir[index]==1:
                    xx = random.randrange(px+1,_r+1,2)
                    self.map[xx][py] = CellState.PATH
                    self.DrawRectangle(xx,py)
                elif dir[index]==2:
                    yy = random.randrange(_t,py,2)
                    self.map[px][yy] = CellState.PATH
                    self.DrawRectangle(px,yy)
                elif dir[index]==3:
                    yy = random.randrange(py+1,_b+1,2)
                    self.map[px][yy] = CellState.PATH
                    self.DrawRectangle(px,yy)

            # 分开的四个部分又重新生成
            self.DivisionGenerator(_l, px-1, _t, py-1)
            self.DivisionGenerator(px+1, _r, _t, py-1)
            self.DivisionGenerator(_l, px-1, py+1, _b)
            self.DivisionGenerator(px+1, _r, py+1, _b)

    # 从此处进行调用 首先全部初始化为路径，然后再补墙拆墙            
    def DivisionGenerate(self):
        for i in range(0,self.size):
            for j in range(0,self.size):
                if i==0 or j==0 or i==self.size-1 or j==self.size-1:
                    self.map[i][j] = CellState.WALL
                    self.DrawRectangle(i,j,"black",False)
                else:
                    self.map[i][j] = CellState.PATH
                    self.DrawRectangle(i,j,"white",False)

        self.InitGame()
        self.DivisionGenerator(1,self.size-2,1,self.size-2)

    # 随机prime算法 非递归
    """
    1.初始时全是墙
    2.构建一墙一通路形式
    3.随机选择一个通路，并将周围墙入容器，标记该通路
    4.在墙容器中随机选取一堵墙，如果墙两边的通路没有同时被标记，
    则打通该墙，并将原来未被标记的通路周围的墙加入容器，
    然后将该通路标记，最后移除该墙
    5.重复操作 4，直到墙容器为空，说明该算法完成，
    6.最后将被标记的通路清除标记
    """
    def PrimGenerator(self):
        for i in range(self.size):
            for j in range(self.size):
                self.map[i][j] = CellState.WALL
                self.DrawRectangle(i,j,"black",False)

        self.InitGame()

        # 构建墙挖开通路的迷宫,奇数点为通路
        for i in range(1,self.size-1,2):
            for j in range(1,self.size-1,2):
                self.map[i][j]=CellState.PATH
                self.DrawRectangle(i,j,"white",False)
        
        # 一个列表 
        vp = []
        # 奇数
        x = random.randrange(1,self.size-1,2)
        y = random.randrange(1,self.size-1,2)
        temp = Point2(x,y)
        # print(x,y)
        # 周围墙入栈
        if(temp.x - 1 >= 2):
            vp.append(Point2(temp.x - 1,temp.y))
        if(temp.x + 1 <= self.size - 3):
             vp.append(Point2(temp.x + 1, temp.y))
        if(temp.y - 1 >= 2):
            vp.append(Point2(temp.x, temp.y - 1))
        if(temp.y + 1 <= self.size - 3):
            vp.append(Point2(temp.x, temp.y + 1))
        # 标记该处通路
        self.map[temp.x][temp.y] = CellState.FLAG
        
        # 迭代生成迷宫
        pos = 0
        while len(vp)!=0:
            # 随机选择一堵墙
            pos = random.randrange(len(vp))
            temp = Point2(vp[pos].x,vp[pos].y)
            # 记录墙是否打通
            flag = False
            if self.map[temp.x+1][temp.y] == CellState.WALL:
                if self.map[temp.x][temp.y-1] != self.map[temp.x][temp.y+1]:
                    self.map[temp.x][temp.y] = CellState.PATH
                    self.DrawRectangle(temp.x,temp.y)

                    # 对新加入的通路进行标记
                    if self.map[temp.x][temp.y-1] == CellState.FLAG:
                        self.map[temp.x][temp.y+1]=CellState.FLAG
                        temp.y += 1
                    else:
                        self.map[temp.x][temp.y-1] = CellState.FLAG
                        temp.y -= 1
                    flag = True
            
            else:
                if self.map[temp.x-1][temp.y] != self.map[temp.x+1][temp.y]:
                    self.map[temp.x][temp.y] = CellState.PATH
                    self.DrawRectangle(temp.x,temp.y)

                    # 对新加入的通路进行标记
                    if self.map[temp.x-1][temp.y]==CellState.FLAG:
                        self.map[temp.x + 1][temp.y]=CellState.FLAG
                        temp.x += 1
                    else:
                        self.map[temp.x-1][temp.y]=CellState.FLAG
                        temp.x -= 1
                    flag = True
            # 墙被打通
            if flag:
                if temp.x-1>=2 and self.map[temp.x-1][temp.y]==CellState.WALL:
                    vp.append(Point2(temp.x-1,temp.y))
                if temp.x+1 <= self.size-3 and self.map[temp.x+1][temp.y]==CellState.WALL:
                    vp.append(Point2(temp.x+1,temp.y))
                if temp.y-1 >=2 and self.map[temp.x][temp.y-1]==CellState.WALL:
                    vp.append(Point2(temp.x,temp.y-1))
                if temp.y+1 <= self.size-3 and self.map[temp.x][temp.y+1]==CellState.WALL:
                    vp.append(Point2(temp.x,temp.y+1))

            vp[pos] = Point2(vp[-1].x,vp[-1].y)
            vp.pop()

        # 将标记的通路还原成path
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j]==CellState.FLAG:
                    self.map[i][j] = CellState.PATH

   
    # 设置开始和结束
    def InitGame(self):
        self.map[1][0] = CellState.PATH
        # 1 0 对应 15 15+15 30 30+15
        self.DrawRectangle(1, 0, "red", delay=False)
        self.map[self.size - 2][self.size - 1] = CellState.PATH
        self.DrawRectangle(self.size-2, self.size-1, "green", delay=False)

    # 控制台输出，用于调试
    def showAtConsol(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.map[i][j] == CellState.PATH:
                    print(0, end=' ')
                else:
                    print(1, end=' ')
            print()



# if判断,该py文件是否为主动执行，非调用
if __name__ == '__main__':
    root = Tk()
    BaseDesk(root)
    # 消息循环，并保持窗口存在
    root.mainloop()
