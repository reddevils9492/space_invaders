# Space Invaders :: Using python and Turtle

import os
import math
import random
import turtle

class BorderPen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.color("white")
        self.penup()
        self.setposition(-300, -300)
        self.pensize(3)
        self.hideturtle()

    def drawBorder(self, side_length):
        self.pendown()
        for side in range(4):
            self.fd(side_length)
            self.lt(90)

class ScorePen(turtle.Turtle):
    score = 0
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.color("white")
        self.penup()
        self.setposition(-270, 270)
        self.write("SCORE : %s" % self.score, False, align="left", font=("Comic Sans MS", 15, "bold"))
        self.hideturtle()

    def update(self,value):
        self.score += value
        self.clear()
        self.write("SCORE : %s" % self.score, False, align="left", font=("Comic Sans MS", 15, "bold"))




class Player(turtle.Turtle):
    playerspeed = 15
    player_bullet = None
    def __init__(self, gif):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.shape(gif)
        self.setposition(0, -280)
        self.setheading(90)
        
    def moveLeft(self):
        x = self.xcor()
        x -= self.playerspeed
        if x < -280:
            x = -280
        self.setx(x)

    def moveRight(self):
        x = self.xcor()
        x += self.playerspeed
        if x > 280:
            x = 280
        self.setx(x) 

    def getPlayerPosition(self):
        return self.xcor(), self.ycor()   

    def reset(self):
        self.hideturtle() 

class Enemy(turtle.Turtle):
    enemyspeed = 2
    def __init__(self, gif, start_x , start_y):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.shape(gif)
        self.setposition(start_x, start_y)

    def moveLateral(self):
        x =self.xcor()
        x += self.enemyspeed
        self.setx(x)

    def moveVertical(self):
        y = self.ycor()
        y -= 40
        self.sety(y)

    def respawn(self):
        x = random.randint(-200,200)
        y = random.randint(100,250)
        self.setposition(x, y)
    
    def reset(self):
        self.hideturtle()

class Bullet(turtle.Turtle):
    bulletspeed = 30
    bulletstate = "ready"
    player = None
    def __init__(self, gif, player):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.penup()
        self.shape(gif)
        self.player = player
        self.setposition(0, -400)
        self.hideturtle()

    def fireBullet(self):
        if self.bulletstate == "ready":
            os.system("afplay sounds/laser.wav&")
            self.bulletstate = "fire"
            x, y = player.getPlayerPosition()
            self.setposition(x, y)
            self.showturtle()
    
    def reset(self):
        self.bulletstate = "ready"
        self.setposition(0, -400)
        bullet.hideturtle()

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor()-t2.xcor(),2) + math.pow(t1.ycor()-t2.ycor(),2))
    if distance < 15:
        return True 
    else:
        return False       

# Set up screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")


# Draw a border 600x600
border_pen = BorderPen()
border_pen.drawBorder(600)
score_pen = ScorePen()

# Register the GIFs as shapes
turtle.register_shape("gifs/bullet.gif")
turtle.register_shape("gifs/player01.gif")
turtle.register_shape("gifs/invader01.gif")

# Create Player, Bullet and Enemy
player = Player("gifs/player01.gif")
bullet = Bullet("gifs/bullet.gif", player)

no_of_enemies = 5
enemies = []
for i in range(no_of_enemies):
    enemies.append(
        Enemy("gifs/invader01.gif",
        random.randint(-200, 200), 
        random.randint(100, 250)
        )
        )

# Create keyboard binding
turtle.listen()
turtle.onkey(player.moveLeft, "Left")
turtle.onkey(player.moveRight, "Right")
turtle.onkey(bullet.fireBullet, "space")

# Main game Loop
finish_game = False
while not finish_game:
    for enemy in enemies:
        enemy.moveLateral()
        if enemy.xcor() > 280:
            for e in enemies:
                e.moveVertical()
                e.enemyspeed *= -1
        
        if enemy.xcor() < -280:
            for e in enemies:
                e.moveVertical()
                e.enemyspeed *= -1
    
        if isCollision(bullet, enemy):
            os.system("afplay sounds/explosion.wav&")
            bullet.reset()
            enemy.respawn()
            score_pen.update(10)

        if isCollision(enemy, player):
            enemy.reset()
            player.reset()
            print("GAME OVER!")
            finish_game = True

    # Move Bullet
    if bullet.bulletstate == "fire":
        y = bullet.ycor()
        y += bullet.bulletspeed
        bullet.sety(y)

    #Check if Bullet reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet.bulletstate = "ready"




delay = input("Press ENTER to exit game window!")