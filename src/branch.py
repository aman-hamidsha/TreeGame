import pygame as pg
import random
from pygame.math import Vector2
import math

# creates 9 strings corresponding to every possible branch type (eg: "thickmedium", "thinlong" or "thickshort"), then loads pngs with those names (eg: "thinlong.png")
# takes the Branch class and the directory the images are stored in as parameters. Remember to include the slash when specifying the directory (eg: "images/" instead of "images")
# returns a 2d array of these images
def CreateBranchImageList(Branch, dir: str="") -> list:
    girthList  = ["thick", "medium", "thin"]
    lengthList = ["long", "medium", "short"]
    imageList = [[pg.image.load(f"{str}{girth}{length}.png").convert() for length in lengthList] for girth in girthList]

    # prevents a rotation bug
    for i in range(len(imageList)):
        imageList[i][j].set_colorkey((0,0,0))
    
    return imageList


# for testing purposes since the images don't exist yet
def CreateBranchImageListTemp(Branch) -> list:
    imageList = [[pg.Surface((length, Branch.widthList[i])) for length in Branch.lengthList[i]] for i in range(len(Branch.widthList))]

    for i in range(len(imageList)):
        for j in range(len(imageList[i])):
            imageList[i][j].fill(pg.Color("brown"))
            imageList[i][j].set_colorkey((0,0,0))

    return imageList

class Branch:
    # possible lengths of branches
    # index using lengthList[pseudoThickness][pseudoLength]
    # thick branches have a pseudoThickness of 0, thin branches have a pseudoThickness of 2
    # each branch thickness has three possiblePseudolengths, where 0 is the longest
    lengthList = [[200, 150, 120],
                  [150, 110, 70], 
                  [100, 75, 40]]

    # the actual thicknesses of thick, medium and thin branches
    widthList = [20,12,6]

    # used to calculate the x-position of the pivot
    distanceFromMidpoint = 20
    # midpoint = 300

    # CONSTRUCTOR - see planning/branch-uml-explanation.txt
    # can be overloaded
    def __init__(self, *args):
        if (len(args) == 1) and type(args[0]) == Vector2:
            self.RandomConstructor(*args)
        elif (len(args) == 1) and type(args[0]) == int:
            pivot = self.GeneratePivot(args[0])
            self.RandomConstructor(pivot)
        elif (len(args) == 1):
            self.CopyConstructor(*args)
        elif (len(args) == 4):
            self.SpecificConstructor(*args)
        else:
            raise ValueError("unexpected number of arguments")

    def RandomConstructor(self, pivot: Vector2):
        # since values weren't provided, generate a random length and rotation value
        length = random.randint(0,2)
        rotation = random.random()*90-45
        self.SpecificConstructor(pivot, length, rotation, True)

        # because values weren't provided, I assume you're generating branch randomly, in which case it's going to generate offshooting branches randomly for you as well
        self.GenerateChildren()

    def SpecificConstructor(self, pivot: Vector2, pseudoLength: int, rotation: float, isLeft: bool):
        self.pseudoLength = pseudoLength
        self.l = self.lengthList[self.thickness][pseudoLength]
        self.w = self.widthList[self.thickness]
        self.image = self.imageList[self.thickness][pseudoLength]
        self.isLeft = isLeft
        self.children = []
        self.pivot = pivot

        if self.isLeft:
            self.rotation = rotation
        else:
            self.rotation = -rotation

        self.RotateOnPivot()

        # calculate the top left and right corners of the branch (for collision)
        if self.isLeft:
            corner1 = self.pivot + Vector2(self.w/2, -self.w/2).rotate(self.rotation)
            corner2 = self.pivot + Vector2(-self.l+self.w/2, -self.w/2).rotate(self.rotation)
        else:
            corner1 = self.pivot + Vector2(-self.w/2, -self.w/2).rotate(self.rotation)
            corner2 = self.pivot + Vector2(self.l-self.w/2, -self.w/2).rotate(self.rotation)

        if (corner1[0] < corner2[0]):
            self.leftCorner  = corner1
            self.rightCorner = corner2
        else:
            self.leftCorner  = corner2
            self.rightCorner = corner1

    # used to copy branches on the left side of the screen to the right side
    def CopyConstructor(self, branchToCopy: object):
        pivot = Vector2(self.midpoint + (self.midpoint-branchToCopy.pivot[0]), branchToCopy.pivot[1])

        self.SpecificConstructor(pivot, branchToCopy.pseudoLength, branchToCopy.rotation, False)
        
        for childToCopy in branchToCopy.children:
            self.children.append(self.child(childToCopy))

    # rotates the branches around a pivot point (aka the end of the branch they're attached to)
    def RotateOnPivot(self):
        self.image = pg.transform.rotate(self.image, -self.rotation)
        displacementOfCenterOfBranch = Vector2(self.l/2-self.w/2, 0)
        
        if self.isLeft:
            self.newPosCenter = self.pivot - displacementOfCenterOfBranch.rotate(self.rotation)
        else:
            self.newPosCenter = self.pivot + displacementOfCenterOfBranch.rotate(self.rotation)
        self.rect = self.image.get_rect(center = self.newPosCenter)

    # generates offshoot branches from another branch
    def GenerateChildren(self):
        if (self.child != None): # thinbranches don't have offshoots so their child attribute is None, which prevents the GenerateChildren code from running
            
            # create the pivot from which to start generating children
            horizontalDisplacement = self.l-self.w/2
            horizontalDisplacementVector = Vector2(-horizontalDisplacement if self.isLeft else horizontalDisplacement, 0)
            rotatedVector = horizontalDisplacementVector.rotate(self.rotation)
            childPivot = rotatedVector + self.pivot

            # actually generate the children. Will generate between 0 and 3 children
            # if the number of children is low, it's rerolled, effectively meaning that branches have a higher chance of having many children
            randNum = random.randint(0, 3)
            if randNum < 2: randNum = random.randint(0, 3)

            for i in range(randNum):
                self.children.append(self.child(childPivot))

    # draws the branch and its offshoots
    def Draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)
        for child in self.children:
            child.Draw(screen)
    
    def UpdateCollision(self, player):
        collided = False
        newPos = self.CheckPlayerCollision(player)

        for child in self.children:
            if newPos != None:
                return newPos
            
            newPos = child.UpdateCollision(player)

        return newPos

    # HIGHESTPOINT #
    # gets highest (smallest) y-value of a branch and any of its offshoots
    # parameters:
        # b - the branch we want to find the highest y for

    def HighestPoint(self) -> int:
        m = self.rect[1]
        for child in self.children:
            m = min(child.HighestPoint(), m)
        return m

    # LOWESTPOINT #
    # like the above function
    def LowestPoint(self) -> int:
        m = self.rect[1] + self.rect[3]
        for child in self.children:
            m = max(child.LowestPoint(), m)
        return m

    # CHECKPLAYERCOLLISION #
    # checks if the player is colliding with this branch
    # parameters:
        # pg.Rect playerPositionOnPreviousFrame - where the player was last frame
        # pg.Rect playerPosition                - where the player is this frame
    # returns:
        # None if the player isn't colliding with the branch
        # Vector2 representing player's updated position due to collision with the branch otherwise

    def CheckPlayerCollision(self, player) -> Vector2:
        a = player.prevRect.bottomleft
        b = player.prevRect.bottomright
        c = player.rect.bottomleft
        d = player.rect.bottomright

        # the denominator will be zero if the lines are parallel, meaning they won't intersect
        # no intersection means no collision, so we can end the method early
        denominator1 = self.CalculateDenominatorOfLineIntersectionPoint(a, c, self.leftCorner, self.rightCorner)
        if denominator1 == 0: return None

        denominator2 = self.CalculateDenominatorOfLineIntersectionPoint(b, d, self.leftCorner, self.rightCorner)
        if denominator2 == 0: return None

        numerator1X = self.CalculateNumeratorOfLineIntersectionPointX(a, c, self.leftCorner, self.rightCorner)
        numerator2X = self.CalculateNumeratorOfLineIntersectionPointX(b, d, self.leftCorner, self.rightCorner)

        numerator1Y = self.CalculateNumeratorOfLineIntersectionPointY(a, c, self.leftCorner, self.rightCorner)
        numerator2Y = self.CalculateNumeratorOfLineIntersectionPointY(b, d, self.leftCorner, self.rightCorner)

        intersection1 = Vector2(numerator1X/denominator1, numerator1Y/denominator1)
        intersection2 = Vector2(numerator2X/denominator2, numerator2Y/denominator2)

        # make sure that the collision of the two lines is between appropriate bounds
        # basically checks if the collision occurred on the branch, or on the line extrapolated from the branch
        isIntersection1Valid = self.IsIntersectionValid(a, c, intersection1)
        isIntersection2Valid = self.IsIntersectionValid(b, d, intersection2)

        # if there has been a collision within the appropriate bounds, adjust player pos
        if isIntersection1Valid or isIntersection2Valid:

            m = (self.rightCorner[1] - self.leftCorner[1]) / (self.rightCorner[0] - self.leftCorner[0])

            # if the right corner is higher
            if self.leftCorner[1] > self.rightCorner[1]:

                # if the rightmost position of the player is not hanging off the branch
                if d[0] < self.rightCorner[0]:
                    playerBottomY = m*(d[0] - self.leftCorner[0]) + self.leftCorner[1]

                # if the rightmost position of the player is hanging off the branch, just set the player's position to the highest point on the branch
                else:
                    playerBottomY = self.rightCorner[1]

            # if the left corner is higher
            else:

                # if the leftmost position of the player isn't hanging off the branch
                if c[0] > self.leftCorner[0]:
                    playerBottomY = m*(c[0] - self.leftCorner[0]) + self.leftCorner[1]
                
                # if the player is hanging off the left edge of the branch:
                else:
                    playerBottomY = self.leftCorner[1]
            
            # if the player is above the branch, there hasn't been a valid collision but the above code will still run
            if player.rect.bottom <= playerBottomY or player.prevRect.bottom >= playerBottomY:
                return None

            # finally, return the new player position
            return Vector2(c[0], playerBottomY - player.rect.h - 1)
        
        # if there hasn't been a valid collision
        else:
            return None
  
    # stolen from wikipedia (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection)
    def CalculateDenominatorOfLineIntersectionPoint(self, a: Vector2, b: Vector2, c: Vector2, d: Vector2):
        return (a[0] - b[0])*(c[1] - d[1]) - (a[1] - b[1])*(c[0] - d[0])

    def CalculateNumeratorOfLineIntersectionPointX(self, a: Vector2, b: Vector2, c: Vector2, d: Vector2):
        return (a[0]*b[1] - a[1]*b[0])*(c[0] - d[0]) - (a[0] - b[0])*(c[0]*d[1] - c[1]*d[0])

    def CalculateNumeratorOfLineIntersectionPointY(self, a: Vector2, b: Vector2, c: Vector2, d: Vector2):
        return (a[0]*b[1] - a[1]*b[0])*(c[1] - d[1]) - (a[1] - b[1])*(c[0]*d[1] - c[1]*d[0])

    def IsIntersectionValid(self, a: Vector2, b: Vector2, intersection: Vector2) -> bool:
        return max(min(a[0], b[0]), self.leftCorner[0]) <= intersection[0] and intersection[0] <= min(max(a[0], b[0]), self.rightCorner[0])

class ThinBranch(Branch):
    thickness = 2
    child = None

class MediumBranch(Branch):
    thickness = 1
    child = ThinBranch

class ThickBranch(Branch):
    thickness = 0
    child = MediumBranch

    # thickbranches always spawn on the same x-position (on the trunk of the tree), so there's no need to provide an x-argument
    # however, thick branches use the same constructor as any other type of branch, which don't always spawn on the same x-position, so we still need to pass both and x and y to the constructor
    # this is done by generating a vector2 using the provided y and calculating the x from it and then passing the vector2 as the argument
    def GeneratePivot(self, y: int) -> Vector2:
        return Vector2(self.midpoint - self.distanceFromMidpoint, y)

Branch.imageList = CreateBranchImageListTemp(Branch)