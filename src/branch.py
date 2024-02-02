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
    lengthList = [[200, 150, 100],
                  [120, 70, 40], 
                  [52, 36, 20]]

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
            self.rotation = 180-rotation

        self.RotateOnPivot()

    # used to copy branches on the left side of the screen to the right side
    def CopyConstructor(self, branchToCopy: object):
        pivot = Vector2(self.midpoint + (self.midpoint-branchToCopy.pivot[0]), branchToCopy.pivot[1])
        rotation = branchToCopy.rotation + 180

        self.SpecificConstructor(pivot, branchToCopy.pseudoLength, rotation, False)
        
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

            # actually generate the children
            for i in range(random.randint(1, 3)):
                self.children.append(self.child(childPivot))

    # draws the branch and its offshoots
    def Draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)
        for child in self.children:
            child.Draw(screen)

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