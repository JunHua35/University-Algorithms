# Dantzig’s Tableau simplex algorithm

The program will read an input text file (see input lp.prob.txt) specifying a linear program. The linear program by default will be in a standard form. 
This means that the goal is always to maximize a given linear objective function, involving decision variables that are always non-negative, 
subject to a set of linear constraints on the decision variables that are expressed in the form: LHS ≤ RHS.
This algorithm finds an optimal set of values for the decision variables and the resultant evaluation of the objective function given those values.

The program will give the output in the form of a .txt file with the optimal decision variables and the optimal objective variable 

An example: maximize z = x +2y

Subject to the constraints
4x + y <= 44
3x + 2y <= 39
2x + 3y <= 37
y <= 9
-x + y <= 6

Input file: 
# numDecisionVariables
2
# numConstraints
5
#objective
1, 2
# constraintsLHSMatrix
4, 1
3, 2
2, 3
0, 1
-1, 1
# constraintsRHSVector
44
39
37
9
6

Output file:
# optimalDecisions
5, 9
# optimalObjective
23
