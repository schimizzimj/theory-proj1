import time
import sys

# naming conventions and the requirement for command line arguments makes it very
# difficult to import brute-avatar.py for its functions, so need functions are just copied
# here for convenience

# Declare a few global variables
wffs = 0
n_sat = 0
n_unsat = 0     # needed counter variables
given = 0
correct = 0

def read_wff (f):
    # this function parses one wff and stores its information in a python dict
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

def find_first(wff, set_vars):
    for clause in wff['clauses']:
        for item in clause:
            if set_vars[(item >> 1) - 1] is 0:
                return item

def create_output (wff): # used to format output string for each wff
    global given, correct # allow use of counters in function
    output = wff['problem'] + "," + str(wff['nVar']) + "," + str(wff['nClause']) + ","
    output += str(wff['maxLiterals']) + "," + str(len(wff['lits'])) + ","
    if wff['answer'] is 'U':
        output += 'U'
    else:
        output += 'S'
    if wff['testSat'] is not '?': # if answer is given
        given += 1
        if wff['testSat'] is wff['answer']:
            output += ",1,"
            correct += 1
        else:
            output += ",-1,"
    else:
        output += ",0,"
    output += str(wff['time']) # runtime
    if wff['answer'] is not "U": # append assignments
        for i in wff['answer']:
            output += "," + str(i & 1)
    return output

def solve(wff):
    depth = 0 # used to determine whether or not you are at the "root"
    first = 0 # keeps track of first literal assignment used from root
    last_set_var = 0 # last set variable
    setVars = [0] * wff['nVar'] # indicates whether a variable has been set 0 is unset, 1 is true, 2 is False
    tried = 0 # keeps track of whether or not a variable has been tried
    clauses_truths = [0] * wff['nClause'] # keeps track of whether a clause has been declared true
    while True:
        if depth is 0: # at the root
            if first is 0:
                first = find_first(wff, setVars) # returns a first variable to try
            else:
                if tried:
                    # if you tried both possibilities for a variable and still not gotten an answer,
                    # it must be unsatifiable
                    return 'U'
                else:
                    first ^= 1 # try other value for variable
            tried = 1
            setVars = [0] * wff['nVar'] # reset setVars to all zeros
            setVars[(first >> 1) - 1] = (first & 1) + 1 # update appropriate element in setVars
            clauses_truths = [0] * wff['nClause'] # reset clauses_truths to zeros
            last_set_var = first
            depth += 1
        else:
            ind = 1 # track if undetermined clauses are independent
            initial_set = last_set_var # used to track if change was made to the last set variable
            # print "vars: ", setVars
            # print "tried: ", tried
            # print "clauses", wff['clauses']
            # print "truths: ", clauses_truths
            # print "last: ", last_set_var
            for i, clause in enumerate(wff['clauses']): # for loop to check switch clauses to true
                if not clauses_truths[i]: # only check clauses that aren't already true
                    if last_set_var in clause:
                        clauses_truths[i] = 1 # set clause to true
                        ind = 0
            for i, clause in enumerate(wff['clauses']): # for loop to select next variable to flip
                if not clauses_truths[i]:
                    if last_set_var ^ 1 in clause: # if the negation of the last set variable is in the clause
                        ind = 0 # not fully independent
                        found = 0 # variable used to track if
                        for item in clause:
                            if item is not last_set_var ^ 1:
                                if setVars[(item >> 1) - 1] is 0:
                                    # if variable is unset, use as new last set variable
                                    last_set_var = item
                                    setVars[(item >> 1) - 1] = (item & 1) + 1
                                    break
                                else: # if trying to assign two values to same variable
                                    depth = 0
                                    break
                            else: # if a clause is simply two of the negations it's a contradiction
                                  # and you must rechoose the variable
                                if found > 0:
                                    depth = 0
                                    break
                                found += 1



                if initial_set is not last_set_var: # if variable was changed, break out
                    break
            if 0 not in clauses_truths: # if all clauses are true, return True
                return setVars
            elif ind:
                # print "======================================================"
                new_wff = wff # create new wff dict
                new_wff['clauses'] = [clause for i, clause in enumerate(wff['clauses']) if not clauses_truths[i]]
                # create new clause list with a list comprehension
                new_wff['nClause'] = len(new_wff['clauses']) # get new length of clauses
                answer = solve(new_wff) # recursively call solve using it as a smaller problem
                return answer




file_name = sys.argv[1] # get command line arguments
f = open(file_name, 'r') # open given file
current = read_wff(f)
while current: # loop through each wff in input file
    wffs += 1
    start = time.time()
    current['answer'] = solve(current)
    end = time.time()
    if current['answer'] is 'U':
        n_unsat += 1
    else:
        n_sat += 1
    current['time'] = round(abs(end - start) * 1e6, 2) # calculate runtime
    print create_output(current)
    current = read_wff(f)

last_line = (sys.argv[1].split("."))[0] + ",avatar," + str(wffs) + ","
last_line += str(n_sat) + "," + str(n_unsat) + "," + str(given) + "," + str(correct)
print last_line # add final line
f.close() # close file
