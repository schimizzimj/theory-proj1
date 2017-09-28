import time



# Declare functions
def read_wff (file):
    f = open(file, 'w')
    line = f.readline()
    line = line.split(" ")
    wff['problem'] = line[1]
    wff['maxLiterals'] = line[2]
    wff['testSat'] = line[3]
    line = f.readline()
    line = line.split(" ")
    wff['nVar'] = line[2]
    wff['nClause'] = line[3]
    wff['clauses'] = []
    for i in range(0, wff['nClause']):
        line = f.readline()
        line = line.split(" ")
        
        for lit in line:

    return wff

def generate_assignment ():


def verify ():


def create_output ():
