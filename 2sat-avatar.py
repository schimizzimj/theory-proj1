import time
import sys

# naming conventions and the requirement for command line arguments makes it very
# difficult to import brute-avatar.py for its functions, so need functions are just copied
# here for convenience

def read_wff (f):
    # this function parses one wff and stores its information in a python dict
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

def solve(wff):
    depth = 0
    first = 0
    lastSet = 0
    setVars = [0] * wff['nVar'] # indicates whether a variable has been set 0 is unset, 1 is true, 2 is False
    tried = [0] * (2 * wff['nVar'])
    clauses_truths = [0] * wff['nClause']
    while True:
        if depth is 0:
            if 0 not in tried:
                return False
            if first is 0:
                first = wff['clauses'][0][0]
            else:
                print "stuff: ", tried[((first ^ 1) >> 1) + ((first ^ 1) & 1) - 1]
                if tried[((first ^ 1) >> 1) + ((first ^ 1) & 1)]: # if we have tried both for this variable, choose a new one
                    # first = 0
                    # i = 0
                    # print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%here"
                    # while not first and i < wff['nClause']:
                    #     for lit in wff['clauses'][i]:
                    #         if not tried[lit - 2]:
                    #             first = lit
                    #     i += 1
                    return False
                else:
                    first ^= 1 # try other value for variable
                    print first
            tried[(first >> 1) + (first & 1) - 1] = 1
            setVars = [0] * wff['nVar'] # reset setVars to all zeros
            setVars[(first >> 1) - 1] = (first & 1) + 1
            clauses_truths = [0] * wff['nClause']
            lastSet = first
            depth += 1
            negations = []
        else:
            ind = 1
            initial_set = lastSet
            if lastSet ^ 1 not in negations:
                negations.append(lastSet ^ 1)
            # print "vars: ", setVars
            # print "tried: ", tried
            # print "clauses", wff['clauses']
            # print "truths: ", clauses_truths
            # print "last: ", lastSet
            # print "negations: ", negations
            for i, clause in enumerate(wff['clauses']):
                if not clauses_truths[i]:
                    if lastSet in clause:
                        clauses_truths[i] = 1
                        ind = 0
                        continue
            for i, clause in enumerate(wff['clauses']):
                if not clauses_truths[i]:
                    # if lastSet ^ 1 in clause:
                    if [i for i in negations if i in clause]:
                        ind = 0
                        found = 0
                        for item in clause:
                            if item is not lastSet ^ 1:
                                if setVars[(item >> 1) - 1] is 0:
                                    lastSet = item
                                    setVars[(item >> 1) - 1] = (item & 1) + 1
                                    break
                                else:
                                    depth = 0
                                    break

                            else:
                                if found > 0:
                                    depth = 0
                                    break
                                found += 1



                if initial_set is not lastSet:
                    break
            if 0 not in clauses_truths:
                return True
            elif ind:
                print "======================================================"
                new_wff = wff
                new_wff['clauses'] = [clause for i, clause in enumerate(wff['clauses']) if not clauses_truths[i]]
                new_wff['nClause'] = len(new_wff['clauses'])
                if len(new_wff['clauses']) > 0:
                    answer = solve(new_wff)
                    return answer
                else:
                    wff['end'] = setVars
                    return True



file_name = sys.argv[1]
f = open(file_name, 'r')
current = read_wff(f)
i = 13
while i:
    print("Ours: {}    Expected: {}").format(solve(current), current['testSat'])
    current = read_wff(f)
    i -= 1
    print "--------------------------", current['problem'] - 1, "------------------------------"
