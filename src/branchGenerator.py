# contains methods used to randomly generate branches
import time

import pygame as pg

import random
from src import branch

class BranchGenerator():
    # CONSTRUCTOR #
    # generates branches and makes sure that you can jump from one to the other, unless you're a nitwit and break them
    # parameters:
        # maxHeight - vertical distance between the bottom of the tree and the finish line
        # jumpHeight - how high the character can jump
        # lowest - the point at which branches will start to generate
    # returns:
        # list of branches, from lowest to highest
    def __init__(self, maxHeight: int, jumpHeight: int, lowest: int) -> list:
        # the maximum height we have reached so far. Keeps track of how close we are to the finish line
        # aka highest point on the highest branch
        topHeight = lowest

        # y-level of where the last branch connected with the tree
        generationHeight = lowest

        # list where we'll store our branches
        branches = []

        # we won't generate branches higher than the player can jump, but we also don't want to force the player to do some pixel-perfect jump to reach the next branch
        # to solve this, give some pixels such that the player can drop down
        padding = 10

        # stops branches generating too high or too low. If they are generating too high or too low, tweak these numbers
        # basically, the branch will generate x pixels above the branch beneath it, where x is a random number between the upper and lower bounds
        # generationUpperBound = jumpHeight + 150
        generationLowerBound = jumpHeight - 30

        # actually, scrap that. The generation is sometimes really slow because the branches that we're randomly generating don't meet a set of criteria, so we need to re-generate them
        # this took ages, so I made a currentUpper variable, which increments when a branch is scrapped because it doesn't meet the criteria
        # it's reset when a new branch is created
        # it basically expands the range in which you can make branches. Bigger range means more possibilities for branch to be functional
        currentUpper = jumpHeight

        while topHeight > maxHeight:
            currentUpper += 20
            # position of the last branch is topHeight, so this number generates a branch x pixels above the branch beneath it
            randomPos = generationHeight - random.randint(generationLowerBound, currentUpper)
            b = branch.ThickBranch(int(randomPos))

            # print(f"randomPos: {randomPos}, generationheight: {generationHeight}, lowestPoint: {b.LowestPoint()}, topheight: {topHeight}, ({topHeight - b.LowestPoint()} < {jumpHeight - padding})")
            # time.sleep(1)
            
            # check if the distance between the two branches is less than the jump height, meaning that the player will be able to jump from the lower branch to the higher branch
            if (topHeight - b.LowestPoint() < jumpHeight - padding):

                # also an additional check to make sure that the branches aren't too low - if they're too low, they overlap with other branches a lot and it gets super messy
                if  (jumpHeight/4 < topHeight - b.LowestPoint()):

                    # the player can reach the branch, that means that the branch is acceptable and we add it to the list and update topHeight and generationHeight
                    topHeight = b.HighestPoint()
                    generationHeight = b.pivot[1]
                    branches.append(b)

                    currentUpper = jumpHeight

            # if the branch was too high to reach via a jump, it's bad generation, so go to the beginning of the while loop and try again
        
        self.branchesL = branches

        # copying all the branches so that they face right as well
        self.branchesR = []
        for b in branches:
            self.branchesR.append(branch.ThickBranch(b))

    # DRAW #
    # Draws all the on-screen branches
    # parameters:
        # screen       - the screen to draw the branches onto
        # screenBottom - the y-value of the bottom of the screen
        # screenTop    - the y-value of the top of the screen
            # these two values are used to determine which branches are on-screen. No point drawing branches that aren't on-screen
    def Update(self, screen: pg.Surface, screenBottom: int, screenTop: int, player):
        
        collidedL = collidedR = False

        for i in range(len(self.branchesL)):

            # check to see if any of the branch is on screen
            if (self.branchesL[i].HighestPoint() < screenBottom and self.branchesL[i].LowestPoint() > screenTop):
                self.branchesL[i].Draw(screen)

                if not collidedL:
                    newPos = self.branchesL[i].UpdateCollision(player)
                    if newPos != None:
                        collidedL = True
                        player.rect.topleft = newPos

                # since we know that the right branches mirror the left branches, if a left branch is visible, so is a right branch, so we don't need to run the if statement separately for the right branches
                self.branchesR[i].Draw(screen)