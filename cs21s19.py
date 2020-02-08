from random import *
from graphics import Rectangle, Circle, Point
from math import sqrt
import os.path as osp


def randBoolean():
  """
    Purpose: return random True/False value
    Parameters: none
    Return: choice, a random boolean val.
  """
  return randrange(2) ==1

def dist(pt1,pt2):
  """
    Params: pt1,pt2: 2 Point objects
    Returns: Euclidean distance between them
  """
  return sqrt((pt2.getY() - pt1.getY())**2 +
              (pt2.getX() - pt1.getX())**2)

def inside(rect, pt):
    x1 = rect.getP1().getX()
    x2 = rect.getP2().getX()
    if(x1>x2):
        temp= x1
        x1 = x2
        x2 = temp

    y1 = rect.getP1().getY()
    y2 = rect.getP2().getY()
    if(y1>y2):
        temp = y1
        y1 = y2
        y2 = temp

    return (x1<= pt.getX() and pt.getX() <= x2 and
            y1 <= pt.getY() and pt.getY() <= y2)

def intersect(rect, circ):
  """
    Params: rect, a Rectangle object
      circ, a Circle object
    Returns: True if rect,circ intersect
  """
  # first, see if rect invades circ
  pt1 = rect.getP1()
  pt2 = rect.getP2()
  center = circ.getCenter()
  rad = circ.getRadius()

  if(dist(pt1,center) <= rad or
     dist(pt2,center) <= rad or
     dist(Point(pt1.getX(), pt2.getY()),center) <= rad or
     dist(Point(pt2.getX(), pt1.getY()),center) <= rad):
     return True

  # then, see if circ invades rect
  cpts = [Point(center.getX() + rad, center.getY()),
          Point(center.getX() - rad, center.getY()),
          Point(center.getX(), center.getY() + rad),
          Point(center.getX(), center.getY() - rad)]

  for pt in cpts:
      if inside(rect, pt):
          return True

  return False

def mysterySearchA(ls, x):
    """
    mystery search function
    is it linear search or binary search?
    params: ls, a list; x, an item
    returns: True if x is item in ls, False otherwise
    """
    for item in ls:
        if (x == item):
            return True
    return False

def mysterySearchB(ls, x):
    """
    mystery search function
    is it linear search or binary search?
    params: ls, a list; x, an item
    returns: True if x is item in ls, False otherwise
    """
    low = 0
    high = len(ls)-1
    while(low<=high):
        mid = (low+high)//2
        if(x == ls[mid]):
            return True
        elif(x < ls[mid]):
            # go left
            high=mid-1
        else:
            #go right
            low=mid+1
    return False

def getIgnoreWords(ignoreFile=".ignorewords"):
    """
    get dictionary of words to ignore
    ignoreFile is text file with one word per line
    throws IOError if file does not exist
    """
    d = {}
    #get current directory of this module
    here = osp.dirname(__file__)
    with open(osp.join(here,ignoreFile)) as f:
        for line in f:
           word = line.strip()
           d[word] = True
    return d

def getWords():
    """
    get  and list of 5 letter English dictionary words that are
    not proper nouns
    """
    ans = []
    try:
      ignore = getIgnoreWords()
    except IOError as e:
      ignore = {}
    with open("/usr/share/dict/words") as f:
        for line in f:
            word = line.strip()
            if word.islower() and word.isalpha() and len(word)==5:
                if word not in ignore:
                  ans.append(word)
    return ans

if __name__ == "__main__":
    ls = getWords()
    shuffle(ls)
    print(ls[:10])
