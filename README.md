## Implementing Amoeba-SAT algorithm to solve SAT in Python 
Amoeba-Inspired Algorithm to solve Boolean Satisfiability Problem(SAT). Implementation of the Algorithm by Masashi Aono et al.(2015). The paper can be accessed in https://www.academia.edu/12342014/Amoeba-inspired_Spatiotemporal_Dynamics_for_Solving_the_Satisfiability_Problem

### Files
- *myAmbSAT.py* - functions for running, to execute run `python3 myAmbSAT.py` and specify the file to execute
- *trials_code.py* - solve for a directory of problems in parallel `python3 trials_code.py` and it will solve for the directory *uf20-91-1* and save the solutions to folders
- *uf20-01000.cnf* - input SAT problem of 20 variables and 91 clauses, took 630 iterations to run with the program, more SAT problem can be found at https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html
- *uf20-91-1* - diectory with 10 SAT problems of 20 variables and 91 clauses, took 13406 iterations to run with the program
- *uf50-01000.cnf* - input SAT problem of 50 variables and 218 clauses
