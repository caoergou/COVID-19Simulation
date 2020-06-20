## 【python】利用turtle库可视化模拟新冠疫情

## 高阶版运行结果展示

![运行过程截图](https://img-blog.csdnimg.cn/20200619205606844.gif#pic_center)



*随着模拟程序的运行，图中的点会逐渐由绿色变红，最终图中的点全部变为灰色，并不再移动。*

*点的颜色不同分别代表个体处于不同的健康状态：**绿色为健康，黄色为潜伏期，红色为感染，而灰色则代表死亡。***

*计算机以绝对理性且冰冷的态度追随代码的运行让一个个点在无序运动逐渐变化颜色*，*但这却是2020年新冠肺炎爆发以来无数条因此丧生的鲜活生命。*

*愿疫情早日结束！*

## 代码讲解

### 基础版：模拟新冠疫情爆发早期，新冠病毒刚开始出现

1.  面向对象：设计人的类应有的方法和属性
    - 属性：
      - 健康状态 `status`，分为`健康`和`患病`
      - 此时人们没有在意健康问题，都不戴口罩
    - 方法
      - `__init__`：定义对象的属性
      - `move`：人的随机运动
      - `infect`：健康人与患者距离小于50，则有50%的概率感染
2.  画布尺寸：设置人员位置，活动范围
3.  实现病毒的传播，即新冠肺炎可以由患者传染给健康的人

#### python代码

``` python
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
        if - TOTAL_W*0.9 < self.x + dx < TOTAL_W*0.9:
            self.x+=dx
        else:
            self.x-=dx
        if - TOTAL_W*0.9 < self.y + dy < TOTAL_W*0.9:
            self.y+=dx
        else:
            self.y-=dy
        #如果他们超出了边界就会往回走
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
```



####  运行截图

<img src="C:\Users\景程\AppData\Roaming\Typora\typora-user-images\image-20200616215232121.png" alt="image-20200616215232121" style="zoom: 50%;" />



### 进阶版：模拟新冠疫情爆发初期，民众防疫意识加强，开始佩戴口罩

1. 面向对象：为人的类`person`添加新的方法和属性

   - 属性：

     - **类属性`total_num`：实验总人数**

     - **类属性`infected_num`：感染人数**

     - 实例属性 `status`，表示该对象的健康状态，分为`健康`和`患病`

     - **实例属性 `mask`，表示该个体是否佩戴口罩，分为`佩戴口罩`和`不佩戴口罩`**

       此时人们开始关注新冠疫情，部分人开始佩戴口罩。
       佩戴口罩可以有效降低感染率（**以下数据为主观猜测，未经验证和校对**）
       具体情况如下：

       | 患者是否佩戴口罩 | 健康人是否佩戴口罩 | 健康人的感染率 |
       | ---------------- | ------------------ | -------------- |
       | 佩戴             | 佩戴               | 1 %            |
       | 佩戴             | 不佩戴             | 15 %           |
       | 不佩戴           | 佩戴               | 30 %           |
       | 不佩戴           | 不佩戴             | 80 %           |

   - 方法

     - `__init__`：定义对象的属性
     - `move`：人的随机运动
     - `infect`：健康人与患者距离小于50，则有根据他们是否佩戴口罩，有不同的概率感**染**

2. **turtle标题可以显示当前天数和感染人数**

3. **引入天数的概念**

``` python
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

class person(object):
    #类属性
    infected_num = 0
    total_num = 0
    def __init__(self,status,mask):
       	person.total_num += 1
        self.turt = turtle.Turtle()
        
        # 是否带口罩，1圆形 为戴口罩/0方形 为不戴口罩，
        self.mask = mask
        if self.mask == 1:
           self.turt.shape('circle')
        elif self.mask == 0:
           self.turt.shape('square')
        
        # 健康状态，1 为确诊/0 为健康
        self.status = status
        if self.status == 1:
            self.turt.color("red")
            self.infected_day = 0
            person.infected_num += 1
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
        if - TOTAL_W*0.9 < self.y + dy < TOTAL_W*0.9:
            self.y+=dx
        else:
            self.y-=dy
        #如果他们超出了边界就会往回走
        self.turt.penup()
        self.turt.goto(self.x, self.y)


    def infect(self,rate):
        x = random.randrange(0,100)
        if x/100 < rate:
            self.status = 1 #此人被感染
            self.infected_day = 0 #有了感染天数，且变为0
            self.turt.color('red')
            person.infected_num+=1 #感染人数+1

    def day(self):
        if self.status == 1:
            self.infected_day += 1
        
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
masked_rate = 0.5 #戴口罩的比例

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
    turtle.title("%d 第 %d 天 已感染人数：%d 总人数：%d"%(count,day,person.infected_num,person.total_num))
    for a in persons:
        for b in persons:
            if id(a)==id(b):
                continue
            elif a.status == 0 and b.status > 0 and dis(a,b) < DANGER_DIS :
                #如果 a 健康，b 感染 ,且距离小于安全距离
                if a.mask == 1 and b.mask == 1:
                    #如果都戴了口罩
                    a.infect(0.01)
                if a.mask == 1 and b.mask == 0:
                    #如果患者b没戴口罩
                    a.infect(0.3)
                if a.mask == 0 and b.mask == 1:
                    #如果a没戴口罩
                    a.infect(0.15)
                if a.mask == 0 and b.mask == 0:
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
        for p in persons:
            p.day()

turtle.bye()
end = datetime.datetime.now()
print("全部感染计算机用时",end-start,"模拟天数:",day,"天")
```

#### 运行截图

<img src="C:\Users\景程\AppData\Roaming\Typora\typora-user-images\image-20200616230021072.png" alt="image-20200616230021072" style="zoom:50%;" />

### 高阶版：模拟新冠疫情爆发中期，人们逐渐了解肺炎的相关性质（潜伏、死亡等）

1. 面向对象：**引入潜伏期和患病天数的概念**，引入死亡的概念

   - 属性：

     - 类属性`total_num`：实验总人数

     - 类属性`infected_num`：感染人数

     - **实例属性 `status`，表示该对象的健康状态，分为`健康`、`潜伏`、`确诊`**

     - **实例属性 `infected_day`，表示患病天数，当患病天数大于4天后有一定概率由潜伏转变为确诊，大于7天有一定概率死亡**

     - 实例属性 `mask`，表示该个体是否佩戴口罩，分为`佩戴口罩`和`不佩戴口罩`

       此时人们开始关注新冠疫情，部分人开始佩戴口罩。
       佩戴口罩可以有效降低感染率（**以下数据为主观猜测，未经验证和校对**）
       具体情况如下：

       | 患者是否佩戴口罩 | 健康人是否佩戴口罩 | 健康人的感染率 |
       | ---------------- | ------------------ | -------------- |
       | 佩戴             | 佩戴               | 1 %            |
       | 佩戴             | 不佩戴             | 15 %           |
       | 不佩戴           | 佩戴               | 30 %           |
       | 不佩戴           | 不佩戴             | 80 %           |

   - 方法

     - `__init__`：定义对象的属性
     - `move`：人的随机运动，但是健康患者不会到隔离区，确诊患者只会在隔离区
     - `infect`：健康人与患者距离小于50，则有根据他们是否佩戴口罩，有不同的概率感染
     - **`day`：如果这个人已患病，则调用这个函数其患病天数+1，当患病天数大于最短潜伏期后，一定概率转为确诊，大于最短死亡期后，一定概率死亡**

2. **turtle标题可以显示当前天数、感染人数、死亡人数、总人数**

#### 代码

``` python
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
        if - TOTAL_W*0.9 < self.y + dy < TOTAL_W*0.9:
            self.y+=dx
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
```

运行截图：

<img src="C:\Users\景程\AppData\Roaming\Typora\typora-user-images\image-20200617021130934.png" alt="image-20200617021130934" style="zoom:50%;" />





-------------

思路启发：

- 治愈功能
- 免疫功能
- 隔离功能
- 新冠肺炎和年龄相关，是否加入年龄的属性
- 是否加入性别

注意问题：

- python的turtle库进行模拟，因为极其耗费CPU，计算量太多了，有些功能不好实现，看下面的例子

---------------------------------

### 【已经失败】最终版：模拟新冠疫情爆发后期，政府开始组织治疗、隔离

1. 面向对象：**引入隔离状态和免疫**

   - 属性：

     - 类属性`total_num`：实验总人数

     - 类属性`infected_num`：感染人数

     - 类属性`dead_num`：死亡人数

     - 类属性`isolated_num`：隔离人数

     - 实例属性 `status`，表示该对象的健康状态，分为`健康`、`潜伏`、`确诊`、`免疫` 

       认为`康复`的人具备对新冠肺炎的抵抗力（**仅为主观猜测，未查找相关资料求证**）

     - 实例属性 `infected_day`，表示患病天数，当患病天数大于4天后有一定概率由潜伏转变为确诊，大于7天有一定概率死亡

     - **实例属性`isolated`，表示该对象是否被隔离，一旦确诊立刻送往隔离**

     - 实例属性 `mask`，表示该个体是否佩戴口罩，分为`佩戴口罩`和`不佩戴口罩`

       此时人们开始关注新冠疫情，部分人开始佩戴口罩。
       佩戴口罩可以有效降低感染率（**以下数据为主观猜测，未经验证和校对**）
       具体情况如下：

       | 患者是否佩戴口罩 | 健康人是否佩戴口罩 | 健康人的感染率 |
       | ---------------- | ------------------ | -------------- |
       | 佩戴             | 佩戴               | 1 %            |
       | 佩戴             | 不佩戴             | 15 %           |
       | 不佩戴           | 佩戴               | 30 %           |
       | 不佩戴           | 不佩戴             | 80 %           |

   - 方法

     - `__init__`：定义对象的属性，**但是起始状态健康的人不会出现在隔离区**
     - **`move`：人的随机运动，但是健康患者不会到隔离区，确诊患者只会在隔离区内**
     - `infect`：健康人与患者距离小于50，则有根据他们是否佩戴口罩，有不同的概率感染
     - `day`：如果这个人已患病，则调用这个函数其患病天数+1，当患病天数大于最短潜伏期后，一定概率（诊断率）转为确诊，大于最短死亡期后，一定概率（死亡率）死亡
     - **`isolated`：如果此人确诊，则立即送往隔离区域**
     - **`heal`：对隔离区患者进行治疗，如果治疗成功则变为`免疫`状态**

2. **分配隔离区域为左上区域**

3. ==**编程失败，隔离功能没法写，CPU效率不够，会直接卡死**==