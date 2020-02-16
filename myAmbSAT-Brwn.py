"""
myAmbSAT-Brwn.py

2020 Sayyor Yusupov
A module to implement Amoeba-inspired AmoebaSAT Brownian algorithm for
solving Boolean Satisfiability Problem.
"""

#### Libraries
# Standard library
import random

def user_input():
    """Open the file defined by the user and store all clauses and number
    of variables from the file appropriately
    
    Returns:
        clauses (list): stores each clause as a list of strings
        n_vars (int): number of variables in the function
    """
    string = 'Please indicate the destination of the file: '
    file_name = input(string)
    # writing each clause as a list inside one list
    clauses = []
    with open(file_name) as f:
        for line in f:
            if len(line)!=0:
                if line[0] == 'p':
                    # number of variables as indicated in the file
                    n_vars = int(line.split()[2])
                elif line[0] not in ('c','%'):
                    clause = []
                    for n in line.split(" "):
                        if n != "0\n":
                            clause.append(n)
                    if len(clause) >= 3:
                        clauses.append(clause)
    # removing blank space in the first line
    if clauses[0][0]=="":
        clauses[0] = clauses[0][1:]
    return clauses, n_vars

def create_INTRA(n_vars):
    """Create ruleset INTRA (used to forbid assignment of both 0 and 1
    to a variable) for the particular problem.
    
    Args:
        n_vars (int): number of variables in the function
    
    Returns:
        INTRA (list): stores each INTRA rule as a list of strings
    """
    INTRA=[]
    for i in range(1,n_vars+1):
        INTRA.append([str(i)+'0',str(i)+'1'])
        INTRA.append([str(i)+'1',str(i)+'0'])
    return INTRA

def create_INTER(clauses):
    """Create ruleset INTER (used to maintain at least one True value
    in each given clause) for the particular problem

    Args:
        clauses (list): stores each clause as a list of strings
    
    Returns:
        INTER (list): stores each INTER rule with P and Q as elements
    """
    INTER = []
    for clause in clauses:
        # storing all variable with their False states
        vars1 = []
        for var in clause:
            if int(var)<0: #if the considered variable has NOT operator
                vars1.append(str(abs(int(var)))+'1')
            else:
                vars1.append(var+'0')
        #storing each rule with first element being P, second - being Q
        for idx,var in enumerate(vars1):
            rule = [] 
            rule.append(vars1[:idx])
            rule[0]+=vars1[idx+1:]
            rule.append(var)
            INTER.append(rule)
    return INTER

def create_CONTRA(INTER):
    """Prevent variables from not being assigned to any value because
    of some rules in the ruleset INTER

    Args:
        INTER (list): stores each INTER rule with P and Q as elements
    
    Returns:
        CONTRA (list): stores each CONTRA rule as a list of strings
    """
    #getting rules with the same output
    out_reps = {}
    for rule in INTER:
        if rule[1] not in out_reps:
            out_reps[rule[1]]=[]
        out_reps[rule[1]].append(rule[0])
    CONTRA=[]
    done=[] # for storing units which were already considered
    for var in out_reps:
        if var[-1]=='1':
            if var not in done:
                for i in out_reps[var]:
                    for j in out_reps[var[:-1]+'0']: #the opposite unit
                        # adding the two Ps
                        # set is for removing duplicates
                        rule1=list(set(i+j))
                        if rule1 not in CONTRA: #avoiding duplicates
                            CONTRA.append(rule1)
                done+=var
    return CONTRA

def run_Z(Z):
    """Generate random real numbers for each unit
    
    Args:
        Z (dict): previous Z-values of each unit
        
    Returns:
        Z (dict): new Z-values of each unit
    """
    for var in Z:
        Z[var] = random.random()
    return Z

def run_Y(Y, Z, e, L):
    """Determine supply or non-supply of resources for each unit
    
    Args:
        Y (dict): previous Y-values of each unit
    
    Returns:
        Y (dict): new Y-values of each unit
    """
    for var in Y:
        if 1-e-Z[var]>0 and L[var]==0: 
            Y[var]=1
        else: #bounceback stimulus is applied
            Y[var]=0
    return Y

def run_X(X,Y):
    """Change the state of each unit according to supply of the
    resources to each unit
    
    Args:
        X (dict): previous X-values of each unit
        
    Returns:
        X (dict): new X-values of each unit
    """
    for var in X:
        if (Y[var]==1) and (X[var]<1):
            X[var]+=1
        elif (Y[var]==0) and (X[var]>-1):
            X[var]-=1
    return X

def run_L(X,L,INTRA,INTER,CONTRA):
    """Determine the need of inhibiting stimulus to each unit based on
    the rulesets

    Args:
        X (dict): current X-values of each unit
        L (dict): previousi L-values of each unit
        INTRA (list): stores each INTRA rule as a list of strings
        INTER (list): stores each INTER rule with P and Q as elements
        CONTRA (list): stores each CONTRA rule as a list of strings
    
    Returns:
        L (dict): new L-values of each unit
    """
    for var in L:
        L[var]=0

    for rule in INTRA:
        if X[rule[0]]==1:
            L[rule[1]]=1
        
    for rule in INTER:
        # checking if the whole set of units have a value 1
        satisfied = True  
        for var in rule[0]:
            if X[var]!=1:
                satisfied=False
                break
        if satisfied:
            L[rule[1]]=1
            
    for rule in CONTRA:
        # checking if the whole set of units have a value 1
        satisfied = True 
        for var in rule:
            if X[var]!=1:
                satisfied=False
                break
        if satisfied:
            for var in rule:
                L[var]=1
    return L

def run_x(x,X):
    """Determine the resulting state of variables based on units in the
    system

    Args:
        X (dict): current X-values of each unit
        
    Returns:
        x (dict): current x-values of each unit
    """
    for var in x:
        if (X[var+'1']<=0 and X[var+'0']==1):
            x[var]=0
        elif (X[var+'1']==1 and X[var+'0']<=0):
            x[var]=1
    return x

def check_solved(X,L):
    """Check if the system is stable (the problem is solved).
    
    Args:
        X (dict): current X-values of each unit
        L (dict): L-values of each unit for the next loop
    
    Returns:
        solved (bool): is the system stable?
    """
    solved=False
    satisf=True
    for var in X:
        if not((X[var]==1 and L[var]==0) or (X[var]<=0 and L[var]==1)):
            satisf = False
            break
    if satisf:
        solved = True
    return solved

def check_solution(clauses,x):
    """Check the statements of each clauases in a function based on a 
    set of inputs
    
    Args:
        clauses (list): stores each clause as a list of strings
        x (dict): current x-values of each unit
    """
    satisf=0 # for storing number of T states
    no_satisf=0 # for storing number of F states
    y1 = [0,0,0] # for storing state of each variable in a clause
    for clause in clauses:
        for idx,var in enumerate(clause):
            # no NOT operator and T
            if int(var)>0 and x[str(abs(int(var)))]==1:
                y1[idx]=1
            # no NOT operator and F
            elif int(var)>0 and x[str(abs(int(var)))]==0:
                y1[idx]=0
            # has NOT operator and T
            elif int(var)<0 and x[str(abs(int(var)))]==1:
                y1[idx]=0
            # has NOT operator and F
            elif int(var)<0 and x[str(abs(int(var)))]==0:
                y1[idx]=1
        # if at least one of the states in the clause is T
        if y1[0]==1 or y1[1]==1 or y1[2]==1:
            satisf+=1
        else:
            no_satisf+=1
    string = (
        "Proportion of T and F states in the function with "
        "resulting variables is: "
    )
    string += str(satisf)+"/"+str(no_satisf)
    print(string)

def main():
    """The main function which combines all other functions"""
    clauses, n_vars = user_input()
    X={}
    Y={}
    Z={}
    L={}
    x={}
    for i in range(1,n_vars+1):
        X[str(i)+'0'] = 0
        X[str(i)+'1'] = 0
        Y[str(i)+'0'] = 0
        Y[str(i)+'1'] = 0
        Z[str(i)+'0'] = 0
        Z[str(i)+'1'] = 0
        L[str(i)+'0'] = 0
        L[str(i)+'1'] = 0
        x[str(i)] = 0
    
    # creating rulesets
    INTRA = create_INTRA(n_vars)
    INTER = create_INTER(clauses)
    CONTRA = create_CONTRA(INTER)

    count=0
    solved = False
    e=0.1 # parameter eta which can be changed
    while not solved:
        count+=1
        Z = run_Z(Z)
        Y = run_Y(Y,Z,e,L)
        X = run_X(X,Y)
        L = run_L(X,L,INTRA,INTER,CONTRA)
        x = run_x(x,X)
        solved = check_solved(X,L)

    # outputing resulting states of the variables
    string = ""
    for var in sorted(x, key=lambda x: int(x)):
        string+=var+": "+str(x[var])+"; "
    print(string+'\n')
    string = "It took total of "+str(count)
    string += " iterations to find the variables"
    print(string+'\n')
    check_solution(clauses,x)

if __name__ == "__main__":
    main()