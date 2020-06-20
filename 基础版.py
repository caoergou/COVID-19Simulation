# 相关类库的导入
import math
import random
import turtle
import time
import datetime

# 有关参数的定义
TOTAL_W = 500 #模拟场地总宽度
TOTAL_H = 400 #模拟场地总高度
DANGER_DIS = 50 #传染距离
RATE = 0.5  #传染率

class person(object):
    def __init__(self,status):
        self.turt = turtle.Turtle()
        self.turt.shape('circle')

        # 健康状态，1 为确诊 0 为健康
        self.status = status
        if self.status == 1:
            self.turt.color("red")
        else:
            self.turt.color("green")
        
        
        #随机定义该点的位置
        self.x = random.randint(-TOTAL_W*0.9,TOTAL_W*0.9)
        self.y = random.randint(-TOTAL_H*0.9,TOTAL_H*0.9)
        
        self.turt.penup()
        self.turt.goto(self.x,self.y)


    def move(self):
        dx = random.randint(-2, 2)
        dy = random.randint(-2, 2)
        self.x+=dx
        self.y+=dy
        #如果他们超出了边界就会往回走
        if self.x <= -TOTAL_W*0.9 or self.y >= TOTAL_W*0.9:
            self.x-=2*dx
        if self.y <= -TOTAL_H*0.9 or self.y >= TOTAL_H*0.9:
            self.y-=2*dy
        self.turt.penup()
        self.turt.goto(self.x, self.y)

    def infect(self,rate):
        x = random.randrange(0,100)
        # 根据传入的感染率的参数
        if x/100 < rate:
            self.status = 1 #此人被感染
            self.turt.color('red')
        
    def reset(self):
        self.turt.penup()
        self.turt.setpos(self.pos)

        
# 距离计算函数，计算两个人之间的距离
def dis(a,b):
    d = math.sqrt((a.x-b.x)**2 + (a.y - b.y)**2)
    return d



# turtle的相关设定
turtle.setup(TOTAL_W*2+200,TOTAL_H*2,0,0)
turtle.screensize(TOTAL_W, TOTAL_H)
turtle.clearscreen()
turtle.hideturtle()
turtle.tracer(False)


# 实验的人数参数设定
total_num = 100
infected_num = random.randint(0,total_num) # 这里以随机数确定起始感染人数
healthy_num = total_num - infected_num

# 所有人的数组
persons = []

# 健康人
for i in range(healthy_num):
    t1 = person(0)
    persons.append(t1)

# 患者
for i in range(infected_num):
    t1 = person(1)
    persons.append(t1)

# 记录程序开始运行的时间
start = datetime.datetime.now()

while infected_num<total_num:
    # 遍历每两个人
    for a in persons:
        for b in persons:
            if id(a)==id(b):
                continue
            elif a.status == 0 and b.status > 0 and dis(a,b) < DANGER_DIS :
                #如果 a 健康，b 感染 ,且距离小于安全距离，则a可能被感染
                    a.infect(RATE)
    # 每个人都会运动
    for a in persons:
          a.move()
    turtle.update()
    time.sleep(1 / 300)
 
turtle.bye()
end = datetime.datetime.now()
print("全部感染计算机用时",end-start)