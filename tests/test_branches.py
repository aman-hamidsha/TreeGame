# run tests with the following command:
# python3 -m unittest discover -p "test_*.py"
# call from the TreeGame directory

import unittest
import pretty_errors
import sys, os

from pygame.math import Vector2

# adds src to path so this file can use stuff from there, like the Branch class
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "..", "src"))

from branch import *

class TestBranches(unittest.TestCase):
    Branch.midpoint = 0

    def test_CreateImageListTemp(self):
        self.assertEqual(Branch.imageList[0][0].get_size(), (Branch.lengthList[0][0], Branch.widthList[0]))
        self.assertEqual(Branch.imageList[2][2].get_size(), (Branch.lengthList[2][2], Branch.widthList[2]))

    def test_ThickBranchHasThickness0(self):
        self.assertEqual(ThickBranch.thickness, 0)

    def test_ThickBranchHasChildMediumBranch(self):
        self.assertEqual(ThickBranch.child, MediumBranch)

    def test_OffshootBranchIsLeftOfMainBranch(self):
        branch1 = ThickBranch(0)
        while len(branch1.children) == 0:
            branch1 = ThickBranch(0)
        
        self.assertTrue(branch1.children[0].pivot[0] < branch1.pivot[0])
    
    def test_BranchSpecifiedToGrowRightActuallyGrowsRight(self):
        branch1 = ThickBranch(Vector2(0,0), 0, 0, False)
        self.assertFalse(branch1.isLeft)

    def test_CopiedBranchIsNotLeft(self):
        branch1 = ThickBranch(0)
        branch2 = ThickBranch(branch1)
        self.assertFalse(branch2.isLeft)
    
    def test_AllChildrenCopied(self):
        branch1 = ThickBranch(0)
        branch2 = ThickBranch(branch1)
        self.assertEqual(self.CountChildren(branch1), self.CountChildren(branch2))

    def CountChildren(self, branch: object, sum: int=0) -> int:
        sum += 1
        for child in branch.children:
            sum = self.CountChildren(child, sum)
        return sum

    def test_LineIntersection(self):
        cases = [
            [Vector2(0, 0), Vector2(2, 2), Vector2(0, 2), Vector2(2, 0), Vector2(1, 1)],
            [Vector2(-3, 1), Vector2(1, -1), Vector2(-1, 1), Vector2(-1, -1), Vector2(-1, 0)],
            [Vector2(3, 0), Vector2(3, -2), Vector2(-2, -1), Vector2(4, -1), Vector2(3, -1)],
            [Vector2(-3, -1), Vector2(-3, 0), Vector2(-2, -2), Vector2(-1, -2), Vector2(-3, -2)]
        ]

        branch1 = ThickBranch(0)
        
        for case in cases:
            self.assertEqual(
                Vector2(
                    branch1.CalculateNumeratorOfLineIntersectionPointX(case[0], case[1], case[2], case[3])/branch1.CalculateDenominatorOfLineIntersectionPoint(case[0], case[1], case[2], case[3]),
                    branch1.CalculateNumeratorOfLineIntersectionPointY(case[0], case[1], case[2], case[3])/branch1.CalculateDenominatorOfLineIntersectionPoint(case[0], case[1], case[2], case[3])
                ),
                case[4]
            )
    
    def test_IsIntersectionValid(self):
        branch1 = ThickBranch(0)
        branch1.leftCorner = Vector2(0, 0)
        branch1.rightCorner = Vector2(2, 0)
        self.assertFalse(branch1.IsIntersectionValid(Vector2(0, 2), Vector2(2, 1), Vector2(4, 0)))


if __name__ == "__main__":
    unittest.main()
