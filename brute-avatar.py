import time
import sys


# Declare functions
def read_wff (f):
    wff = {}
    line = f.readline()
    if not line:
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
    for i in range(0, int(wff['nClause'])):
        line = f.readline()
        line = line.split(",")
        currentClause = []
        for lit in line:
            lit = int(lit)
            if lit < 0:
                currentLit = 2 * abs(lit) + 1
            else:
                currentLit = 2 * abs(lit)
            currentClause.append(currentLit)
            if currentLit not in wff['lits']:
                wff['lits'].append(currentLit)
            if abs(lit) not in wff['vars']:
                wff['vars'].append(abs(lit))
        wff['clauses'].append(currentClause)
    return wff

def generate_assignment ():
    return

def verify ():
    return

def create_output ():
    return

file_name = sys.argv[1]
f = open(file_name, 'r')
current = read_wff(f)
while current:
    print current['problem']
    current = read_wff(f)
f.close()
