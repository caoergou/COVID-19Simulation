# 相关类库的导入
import math
import random
import turtle
import time
import datetime


class person(object):
    #类属性
    infected_num = 0
    total_num = 0
    dead_num = 0
    def __init__(self,status,mask):
       	person.total_num += 1
        self.turt = turtle.Turtle()
        
        # 是否带口罩，1为戴口罩 圆形/0为不戴口罩 方形
        self.mask = mask
        if self.mask == 1:
           self.turt.shape('circle')
        elif self.mask == 0:
           self.turt.shape('square')
        
        # 健康状态，2 为确诊 红色/1 为潜伏 黄色/0 为健康 绿色 
        self.status = status
        if self.status == 2:
            self.infected_day = 0
            person.infected_num += 1
            self.turt.color("red")
        elif self.status == 1:
            self.infected_day = 0
            person.infected_num += 1
            self.turt.color("yellow")
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
        if - TOTAL_W*0.9 < self.x + dx < TOTAL_W*0.9:
            self.x+=dx
        else:
            self.x-=dx
        if - TOTAL_H*0.9 < self.y + dy < TOTAL_H*0.9:
            self.y+=dy
        else:
            self.y-=dy
        #如果他们超出了边界就会往回走
        self.turt.penup()
        self.turt.goto(self.x, self.y)


    def infect(self,rate):
        x = random.randrange(0,100)
        if x/100 < rate:
            self.status = 1 #此人的状态进入潜伏期
            self.infected_day = 0 #有了感染天数，且变为0
            self.turt.color('yellow')
            person.infected_num+=1

    def day(self):
        if self.status > 0:
            if self.infected_day >= 7:
                x = random.randrange(0,100)
                if x/100 < DEATH_Rate: #死亡率为5%
                    #确定死亡时返回某个值
                    return -1
        if self.status == 1:
            self.infected_day += 1
            if self.infected_day >= 4:
                x = random.randrange(0,100)
                if x/100 < Diagnose_Rate:
                    self.status = 2
                    self.turt.color('red')
        return 0


    def dead(self):
        # 死亡以后颜色变为灰色
        self.turt.color('gray')
        person.total_num -= 1
        person.dead_num += 1
        if self.status>0:
            person.infected_num -= 1
    
    def __del__(self):
        person.total_num -= 1
        if self.status>0:
            person.infected_num -= 1

        
# 距离计算函数，计算两个人之间的距离
def dis(a,b):
    d = math.sqrt((a.x-b.x)**2 + (a.y - b.y)**2)
    return d



# 有关参数的定义
TOTAL_W = 500 #模拟场地总宽度
TOTAL_H = 400 #模拟场地总高度
DANGER_DIS = 50 #传染距离

#感染率
#W = without Mask 不带口罩
#M = Mask 带口罩
#IR Infection Rate 传染率
#前面的是 患者是否戴口罩
#后面的是 健康是否戴口罩
#值表示的是健康人员的传染概率
IR_WW = 0.8  #双方都不带口罩的传染率
IR_MM = 0.01 #双方都戴口罩的传染率
IR_WM = 0.3  #患病一方不戴口罩，健康者戴口罩
IR_MW = 0.15 #患病一方戴口罩，健康者不戴口罩

#确诊率
Diagnose_Rate = 0.5
#希望率
DEATH_Rate = 0.05

# 实验的人数参数设定
total_num = 100
infected_num = random.randint(0,total_num) # 这里以随机数确定起始感染人数
healthy_num = total_num - infected_num
masked_rate = 0.5 #戴口罩的比例

# turtle的相关设定
turtle.setup(TOTAL_W*2+200,TOTAL_H*2,0,0)
turtle.screensize(TOTAL_W, TOTAL_H)
turtle.clearscreen()
turtle.hideturtle()
turtle.tracer(False)



# 所有人的数组
persons = []

# 类属性的设置（其实可以用类方法）
person.infected_num = 0
person.total_num = 0


# 健康人
for i in range(healthy_num):
    masked = random.random()
    if masked < masked_rate:
        # 如果戴口罩
	    t1 = person(0,1)
    else:
        # 如果不戴口罩
        t1 = person(0,0)
    persons.append(t1)

# 患者
for i in range(infected_num):
    masked = random.random()
    if masked < masked_rate:
    	t1 = person(1,1)
    else:
    	t1 = person(1,0)
    persons.append(t1)



# 记录程序开始运行的时间
start = datetime.datetime.now()
# 开始
day = 0
count = 0
while person.infected_num<person.total_num:
    turtle.title("%d 第 %d 天 现有病例：%d 死亡病例：%d 总人数：%d"%(count,day,person.infected_num,person.dead_num,person.total_num))
    for a in persons:
        for b in persons:
            if id(a)==id(b):
                continue
            elif a.status == 0 and b.status > 0 and dis(a,b) < DANGER_DIS :
                #如果 a 健康，b 感染 ,且距离小于安全距离
                if a.mask == 1 and b.mask == 1:
                    #如果都戴了口罩
                    a.infect(0.01)
                elif a.mask == 1 and b.mask == 0:
                    #如果患者b没戴口罩
                    a.infect(0.3)
                elif a.mask == 0 and b.mask == 1:
                    #如果a没戴口罩
                    a.infect(0.15)
                elif a.mask == 0 and b.mask == 0:
                    #如果都没戴口罩
                    a.infect(0.8)
    for a in persons:
          a.move()
    turtle.update()
    time.sleep(1 / 300)
    count += 1
    # 每次更新100帧率，为一天
    if count > 100:
        day +=1 
        count = 0
        for p in persons[:]:
            if p.day() == -1:
                p.dead()
                persons.remove(p)

turtle.bye()
end = datetime.datetime.now()
print("全部感染计算机用时",end-start,"模拟天数:",day,"天")