#!/usr/bin/env python
# Implemented by Denis Alicic 2018.
import sys,re

solution = {}

def initialize_solution(D):
    for clause in D:
        for literal in clause:
            if literal not in solution and -literal not in solution:
                solution[+literal] = "T" 

def replace_literal(D,literal,key):
    if literal in solution:
        solution[literal] = key
    else:
        solution[-literal] = "T" if key == "F" else "F"
    for i in range(0,len(D)):
        D[i] = list(map(lambda x : x if isinstance(x,basestring) else (key if x == literal else x),D[i]))
    return D

def num_of_literal(D,literal):
     return sum(list(map(lambda x :  x.count(literal) ,D)))

def DPLL(D):
    if len(D) == 0:
        return True
    newD = []
    
    for clause in D:
        clause = list(filter(lambda x: x != "F",clause))
        newD.append(clause)
    D = newD
    for clause in D:
        if len(clause) == 0:
            return False
    # Tautology
    # Droping clauses which has "T"
    newD = list(filter(lambda x : "T" not in x,D))
    # If something happened call recursion 
    if len(D) != len(newD):
        #print("-----TAUTOLOGY------")
        #print(newD)
        return DPLL(newD)
    D = newD
    newD = []
    # Droping clauses which has some literal and its negation
    for clause in D:
        drop = False
        for p in clause:
            if -p in clause:
                drop = True
        if drop == False:
            newD.append(clause)
        

    # If something happened call recursion 
    if len(D) != len(newD):
        #print("-----TAUTOLOGY------")
        #print(newD)
        return DPLL(newD)
    # Unit propagation
    for clause in D:
        if len(clause) == 1:
            if clause[0] > 0:
                #print("----UNIT PROPAGATION-----")
                D = replace_literal(D,clause[0],"T")
                D = replace_literal(D,-clause[0],"F")
                #print(D)
                return DPLL(D)
            else:
                #print("----UNIT PROPAGATION-----")
                D = replace_literal(D,-clause[0],"F")
                D = replace_literal(D,clause[0],"T")
                #print(D)
                return DPLL(D)
    # Pure literal
    for clause in D:
        for p in clause:
            if num_of_literal(D,-p) == 0:
                #print("----PURE LITERAL-----")
                D = replace_literal(D,p,"T")
                #print(D)
                return DPLL(D)
    # SPLIT
    literal = D[0][0]
    #print("------SPLIT-----")
    # Must,because of copying list by reference
    newD = list(D)
    newD = replace_literal(newD,literal,"T")
    newD = replace_literal(newD,-literal,"F")
    #print(newD)
    if DPLL(newD) == True:
        return True
    else:
        #print("------SPLIT-----")
        D = replace_literal(D,literal,"F")
        D = replace_literal(D,-literal,"T")
        #print(D)
        return DPLL(D)


def initialize_data(input_f):
    data = []
    try:
        with open(input_f,"r") as f:
            # Separation tokens
            data = list(map(lambda x : re.split(r'[ ]+',x),f.read().split("\n")))
            # Separation relevant data 
            data = list(filter(lambda x:  x[0] != "p" and x[0] != "c" and len(x) != 1,data))
            # Drop 0 from cnf format
            data = list(map(lambda x: x[0:len(x) - 1],data))
            # Cast in Integer because of easier implementtion of algorithm 
            for i in range(0,len(data)):
                data[i] = list(map(lambda x : int(x),data[i]))
    except IOError:
        print("Error")
        sys.exit(1)
    return data

def main():

    input_f = "input.cnf"
    if len(sys.argv) == 2:
        input_f = sys.argv[1]
    data = initialize_data(input_f)
    initialize_solution(data)
    print(data)

    if DPLL(data):
        print("SAT")
        solution_settled = []
        for (literal,s) in solution.items():
            if s == 'T':
                solution_settled.append(literal)
            else:
                solution_settled.append(-literal)
                
        print(solution_settled)
    else:
        print("UNSAT")
    

if __name__ == "__main__":
    main()
