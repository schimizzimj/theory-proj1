import time
import sys


# Declare a few global variables
wffs = 0
n_sat = 0
n_unsat = 0
given = 0
correct = 0

# Declare functions
def read_wff (f):
    wff = {}
    line = f.readline().strip()
    if not line:
        return
    line = line.split(" ")
    wff['problem'] = line[1]
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

def check_lit (assign, lit):
    return (lit & 1) ^ (get_nth_bit(assign, lit >> 1))

def verify (assign, wff):
    clauses_true = True
    for clause in wff['clauses']:
        this_clause = False
        for lit in clause:
            if check_lit(wff['assignment'], lit):
                this_clause = True
                break
        clauses_true = this_clause
        if not this_clause:
            return False
    if clauses_true:
        return True

def create_output (wff):
    global given, correct
    output = wff['problem'] + "," + str(wff['nVar']) + "," + str(wff['nClause']) + ","
    output += str(wff['maxLiterals']) + "," + str(len(wff['lits'])) + "," + wff['answer']
    if wff['testSat']:
        given += 1
        if wff['testSat'] is wff['answer']:
            output += ",1,"
            correct += 1
        else:
            output += ",-1,"
    else:
        output += ",0,"
    output += str(wff['time'])
    if wff['answer'] is "S":
        for i in range(1, wff['assignment'].bit_length()):
            output += "," + str(get_nth_bit(wff['assignment'], i))
    return output

def get_nth_bit (num, n):
    return (num >> (n - 1)) & 1

file_name = sys.argv[1]
f = open(file_name, 'r')
current = read_wff(f)
while current:
    wffs += 1
    current['assignment'] = 0
    start = time.time()
    while current['assignment'].bit_length() <= len(current['vars']):
        sat = verify(current['assignment'], current)
        if sat:
            break
        current['assignment'] = generate_assignment(current['assignment'])
    if sat:
        current['answer'] = "S"
        n_sat += 1
    else:
        current['answer'] = "U"
        n_unsat += 1
    end = time.time()
    current['time'] = round(abs(end - start) * 1e6, 2)
    return create_output(current)
    current = read_wff(f)

last_line = (sys.argv[1].split("."))[0] + ",avatar," + str(wffs) + ","
last_line += str(n_sat) + "," + str(n_unsat) + "," + str(given) + "," + str(correct)
print last_line
f.close()
