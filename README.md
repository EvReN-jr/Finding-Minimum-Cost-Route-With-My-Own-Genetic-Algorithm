# Finding-Minimum-Cost-Route-With-My-Own-Genetic-Algorithm
We have a global transport company, we have some rules, we searching minimum cost route

Story:
We have a packet and try the best route with information.

Every single transport sector has opening cost and closing cost.

Let's say packet move to from A to D.
B and D are open transport sector.
A and C are close transport sector.
Routes are A-D, A-C-D, A-B-C-D.
A-D: opening cost for A, closing cost for B and transport cost(A->D)
A-C-D: opening cost for A and C and transport cost(A->C->D)
A-B-C-D: A-D: opening cost for A and C and transport cost(A->B->C->D)

Transport sectors are must be enough capacity for transport else route is invalid.

From A to D transport demand must be different to zero.

Must be one way for go to a transport sector.

Every route is optimized in C headers functions.
Rule checking and optimized for routes family in F headers functions.

Routes family is like routes pool.
