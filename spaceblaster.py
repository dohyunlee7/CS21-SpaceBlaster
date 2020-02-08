"""
Dohyun Lee
April 24th, 2019
A program that navigates a starship through space and destroys asteroids
"""
from graphics import *
from random import randrange, uniform, random
from time import sleep
from cs21s19 import intersect
class Asteroid(object):
    def __init__(self,win):
        self.dx = uniform(-1,1)
        self.dy = uniform(-1,1)
        r = randrange(256)
        g = randrange(256)
        b = randrange(256)
        clr = color_rgb(r,g,b)

        if self.dx > 0 and self.dy > 0: #starts from left
            self.ast = Circle(Point(0,uniform(0,100)), uniform(5,10))
            self.ast.setFill(clr)
            self.ast.draw(win)
        elif self.dx > 0 and self.dy < 0: #starts from top
            self.ast = Circle(Point(uniform(0,100),100), uniform(5,10))
            self.ast.setFill(clr)
            self.ast.draw(win)
        elif self.dx < 0 and self.dy < 0: #starts from right
            self.ast = Circle(Point(100,uniform(0,100)), uniform(5,10))
            self.ast.setFill(clr)
            self.ast.draw(win)
        elif self.dx < 0 and self.dy > 0: #starts from bottom
            self.ast = Circle(Point(uniform(0,100),0), uniform(5,10))
            self.ast.setFill(clr)
            self.ast.draw(win)

        self.win = win
        self.value = 0

    def getCenter(self):
        return self.ast.getCenter()

    def getRadius(self):
        return self.ast.getRadius()

    def moveAst(self):
        """
        parameters: self
        purpose: moves asteroid
        """

        self.ast.move(self.dx*2,self.dy*2)

    def offScreen(self):
        """
        parameters: self
        purpose: returns True if Asteroid if offscreen
        """
        ctr = self.ast.getCenter()
        x = ctr.getX()
        y = ctr.getY()
        rad = self.ast.getRadius()
        pos1 = y - rad
        pos2 = y + rad
        pos3 = x + rad
        pos4 = x - rad
        if pos1 > 100 or pos2 < 0 or pos3 < 0 or pos4 > 100:
            return True
        else:
            return False

    def destroy(self):
        """
        parameters: self
        purpose: changes the color of the Circle to signify it has blown up
        """
        self.ast.undraw()
        self.ast.draw(self.win)
        self.ast.setFill("red")
        self.ast.undraw()
        self.ast.draw(self.win)
        self.ast.setFill("teal")
        sleep(0.02)
        self.ast.undraw()

    def getBoundary(self):
        return self.ast.clone()

class Starship(object):
    def __init__(self,win):
        self.ship = Rectangle(Point(45,46),Point(54,50))
        self.ship.setFill("yellow")
        self.fin1 = Rectangle(Point(43,45),Point(47,47))
        self.fin1.setFill("cyan")
        self.fin2 = Rectangle(Point(43,49),Point(47,51))
        self.fin2.setFill("cyan")
        self.ship.draw(win)
        self.fin1.draw(win)
        self.fin2.draw(win)
        self.starship = [self.ship, self.fin1, self.fin2]
        self.speed = 0
        self.direction = "Right"
        self.win = win

    def moveShip(self,new_direction):
        """
        parameters: self, new_direction
        purpose: moves starship using the arrow keys
        """

        if new_direction == self.direction:
            self.speed = self.speed * 1.1
        elif new_direction == "":
            self.speed = 1
            new_direction = self.direction
        else:
            self.speed = 1
        for part in self.starship:
            if new_direction == "Left":
                part.move(-self.speed,0)
            elif new_direction == "Right":
                part.move(self.speed,0)
            elif new_direction == "Up":
                part.move(0,self.speed)
            elif new_direction == "Down":
                part.move(0,-self.speed)
        self.direction = new_direction

    def collide(self, asteroid):
        """
        parameters: self, asteroid
        purpose: takes an asteroid object as input and returns
        True if the starship has collided with this asteroid
        """
        for part in self.starship:
            cross = intersect(part, asteroid)
            if (cross):
                return True
        return False


    def fire(self,asteroids):
        """
        parameters: self, asteroids(list of asteroids)
        purpose: fires a laser
        """
        score=0
        shipCtr = self.ship.getCenter()
        laser = Line(Point(shipCtr.getX()+4.5,shipCtr.getY()), Point(100,shipCtr.getY()))
        laser.draw(self.win)
        laser.setFill("red")
        sleep(0.02)
        for i in range((len(asteroids)-1),-1,-1):
            rockCtr = asteroids[i].getCenter()
            rad = asteroids[i].getRadius()
            if rockCtr.getX() > shipCtr.getX():
                if (shipCtr.getY() <= (rockCtr.getY() + rad)) and (shipCtr.getY() >= (rockCtr.getY() - rad)):
                    asteroids[i].destroy()
                    asteroids.pop(i)
                    score += 1
        laser.undraw()
        return score

def main():
    win = GraphWin("Space Blaster", 800, 800)
    win.setCoords(0,0,100,100)
    win.setBackground("black")
    asteroids = []
    ship = Starship(win)
    for i in range(15):
        asteroids.append(Asteroid(win))
    welcome = Text(Point(50,73),"Welcome to Space Blaster!")
    welcome.setFill("white")
    welcome.setSize(18)
    welcome.draw(win)
    start = Text(Point(50,70), "Click anywhere to begin!")
    start.setFill("white")
    start.setSize(18)
    start.draw(win)
    win.getMouse()
    welcome.undraw()
    start.undraw()
    keyVal = win.checkKey()
    didCol = False
    scoreBoard = Text(Point(50,70), "Score: 0")
    scoreBoard.setFill("white")
    scoreBoard.setSize(18)
    scoreBoard.draw(win)
    score = 0
    while (keyVal != "q") and didCol == False:
        didCol = False
        keyVal = win.checkKey()
        for i in range((len(asteroids)-1),-1,-1):
            ship.moveShip(keyVal)
            asteroids[i].moveAst()
            col = ship.collide(asteroids[i])
            if col == True:
                didCol = True
            if asteroids[i].offScreen() == True:
                asteroids.pop(i)
        if keyVal == "f":
            finalScore = ship.fire(asteroids)
            score += finalScore
            scoreBoard.setText("Score: %d" % (score))

        randNum = random()
        if randNum < 0.01:
            asteroids.append(Asteroid(win))
        sleep(0.1)
    if didCol == True:
        scoreBoard.undraw()
        msg = Text(Point(50,70), """You have crashed into an asteroid
and died a pitiful death. Game Over.""")
        score = Text(Point(50,65), "Your score was %d" % (score))
        msg.setFill("white")
        msg.setSize(18)
        score.setFill("yellow")
        score.setSize(18)
        msg.draw(win)
        score.draw(win)
    else:
        scoreBoard.undraw()
        over = Text(Point(50,70),"You pressed quit. Game Over.")
        score = Text(Point(50,65), "Your score was %d" % (score))
        over.setFill("white")
        over.setSize(18)
        score.setFill("yellow")
        score.setSize(18)
        over.draw(win)
        score.draw(win)

    win.getMouse()
    win.close()
if __name__ == "__main__":
    main()
