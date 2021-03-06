#!/usr/bin/env python
# Implemented by Denis Alicic 2018.
import sys
import re
import argparse

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
    # Droping clauses which have "T" and droping literal "F"
    # So, there's no actually replacing. This is faster solution
    if key == "T":
        return list(filter(lambda x: literal not in x,D))
    else:
        return list(map(lambda clause: list(filter(lambda l: l!= literal,clause)) if literal in clause else clause,D))

def num_of_literal(D,literal):
     return sum(list(map(lambda x :  x.count(literal) ,D)))

def DPLL(D):
    if len(D) == 0:
        return True
    newD = []
    for clause in D:
        if len(clause) == 0:
            return False

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
        return DPLL(newD)
    # Unit propagation call:
    for clause in D:
        if len(clause) == 1:
            if clause[0] > 0:
                D = replace_literal(D,clause[0],"T")
                D = replace_literal(D,-clause[0],"F")
                return DPLL(D)
            else:
                D = replace_literal(D,-clause[0],"F")
                D = replace_literal(D,clause[0],"T")
                return DPLL(D)
    # Pure literal
    for clause in D:
        for p in clause:
            if num_of_literal(D,-p) == 0:
                D = replace_literal(D,p,"T")
                return DPLL(D)
    # SPLIT
    literal = D[0][0]
    # Must,because of copying list by reference
    newD = list(D)
    newD = replace_literal(newD,literal,"T")
    newD = replace_literal(newD,-literal,"F")
    if DPLL(newD) == True:
        return True
    else:
        D = replace_literal(D,literal,"F")
        D = replace_literal(D,-literal,"T")
        return DPLL(D)


def initialize_data(input_f):
    data = []
    try:
        with open(input_f,"r") as f:
            # Separation tokens
            data = list(map(lambda x : re.split(r'[ \t]+',x),f.read().split("\n")))
            # Separation relevant data 
            data = list(filter(lambda x:  x[0] != "p" and x[0] != "c" and len(x) != 1,data))
            # Drop 0 from cnf format
            data = list(map(lambda x: x[0:len(x) - 1],data))
            # Cast in Integer because of easier implementation of algorithm 
            for i in range(0,len(data)):
                data[i] = list(map(lambda x : int(x),data[i]))
    except IOError:
        print("Error")
        sys.exit(1)
    return data

def print_evaluation(shuffled_solution):
    evalution = [None] * len(shuffled_solution)
    for literal in shuffled_solution:
        evalution[abs(literal) - 1] = 1 if literal > 0 else 0
    print("Evaluation: ")
    print(evalution)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        help="Input .cnf file",
        required=True
        )
    args = parser.parse_args()
    data = initialize_data(args.input_file)
    initialize_solution(data)

    if DPLL(data):
        print("SAT")
        solution_settled = []
        for (literal,s) in solution.items():
            if s == 'T':
                solution_settled.append(literal)
            else:
                solution_settled.append(-literal)

        print_evaluation(solution_settled)
    else:
        print("UNSAT")


if __name__ == "__main__":
    main()
