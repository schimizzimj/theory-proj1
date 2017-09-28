import time
import sys


# Declare functions
def read_wff (f):
    line = f.readline()
    if (!line):
        return
    line = line.split(" ")
    wff['problem'] = line[1]
    wff['maxLiterals'] = line[2]
    wff['testSat'] = line[3]
    line = f.readline()
    line = line.split(" ")
    wff['nVar'] = line[2]
    wff['nClause'] = line[3]
    wff['clauses'] = []
    wff['vars'] = []
    wff['lits'] = []
    for i in range(0, wff['nClause']):
        line = f.readline()
        line = line.split(" ")
        currentClause = []
        for lit in line:
            (currentLit = abs(lit) + 1) if (lit < 0) else (currentLit = abs(lit))
            currentClause.push(currentLit)
            if currentLit not in wff['lits']:
                wff['lits'].push(currentLit)
            if abs(lit) not in wff['vars']:
                wff['vars'].push(abs(lit))
    return wff

def generate_assignment ():


def verify ():


def create_output ():

file_name = sys.argv[1]
f = open(file_name, 'r')
while (wff = read_wff(f)):
    print wff['problem']
f.close()
