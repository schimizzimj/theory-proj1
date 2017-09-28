import time
import sys


# Declare functions
def read_wff (f):
    wff = {}
    line = f.readline().strip()
    if not line:
        return
    line = line.split(" ")
    wff['problem'] = int(line[1])
    wff['maxLiterals'] = int(line[2])
    wff['testSat'] = line[3]
    line = f.readline().strip()
    line = line.split(" ")
    wff['nVar'] = int(line[2])
    wff['nClause'] = int(line[3])
    wff['clauses'] = []
    wff['vars'] = []
    wff['lits'] = []
    for i in range(0, int(wff['nClause'])):
        line = f.readline().strip()
        line = line.split(",")
        currentClause = []
        for lit in line:
            lit = int(lit)
            if lit is 0:
                continue
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
    wff['vars'].sort();
    wff['lits'].sort();
    return wff

def generate_assignment (a):
    return a + 1

def verify (assign, lit):
    return (lit & 1) ^ (get_nth_bit(assign, lit >> 1))

def create_output ():
    return

def get_nth_bit (num, n):
    return (num >> (n - 1)) & 1

file_name = sys.argv[1]
f = open(file_name, 'r')
current = read_wff(f)
i = 100
while i is not 0:
    current['assignment'] = 0
    while current['assignment'].bit_length() <= len(current['vars']):
        clauses_true = True
        for clause in current['clauses']:
            this_clause = False
            for lit in clause:
                if verify(current['assignment'], lit):
                    this_clause = True
                    break
            clauses_true = this_clause
            if not this_clause:
                break
        if clauses_true:
            break
        current['assignment'] = generate_assignment(current['assignment'])
    if clauses_true:
        print ("Ours: {}   Expected: {}").format("S", current['testSat'])
    else:
        print ("Ours: {}   Expected: {}").format("U", current['testSat'])

    current = read_wff(f)
    i -= 1
f.close()
