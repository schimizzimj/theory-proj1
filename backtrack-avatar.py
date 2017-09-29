import sys
import time
given = 0
correct = 0
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
        solutions = [-1]*wff['nVar']
        for i in wff['assignment']:
            if i%2 == 0:
                solutions[(i>>1)-1] = 1
            else:
                solutions[(i>>1)-1] = 0
        for j in solutions:
            output += "," + str(j)
    return output

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
def length_compare(x, y):
    return len(x) - len(y)
def satis(wff):
    literals = []#stack of used variables
    flipped = []#stack to represent if each variable has been flipped
    status = []#list keeping track of which clauses are solved
    varstat = [] #variable statuses
    wffsrt = sorted(wff['clauses'], cmp=length_compare)#sort clauses by length
    for q in range(0, len(wff['vars'])+20):
        varstat.append(0)
    varstat[0] = 5
    for x in range(0, len(wffsrt)):#set all statuses to 0
        status.append(0)
    nextlit = wffsrt[0][0]
    flipped.append(0)
    while 1:
    #    print "__++__++__++__++"
    #    for z in status:#subtract one from all status markers
    #        print "status2",z
    #    print "__++__++__++__++"
    #    for x in varstat:
    #        print x
    #    for x in literals:
    #        print "literal:",x
    #    print "nextlit",nextlit
        literals.append(nextlit)#push first variable to stack
        thevar = nextlit>>1
        if nextlit%2 == 0:
            varstat[thevar] = 2
        else:
            varstat[thevar] = 1
        i = 0#counter
        bad = 0
        #checks if a clause is unsatisfiable
        for x in wffsrt:#for each clause check if solved and mark if so
            if status[i] > 0:
                status[i] = status[i] + 1 #add one step to all satisfied clauses
            if literals[-1] in x and status[i]==0: #check which clauses are now good
                status[i] = 1
            if status[i]==0: # see if any statuses are unsatisfiable
                g = 0
                for y in x:
    #                print "***",y,"***",y^1,"***"
                    if y^1 not in literals and y > 1:
                        g = 1
    #                print "g,",g
                if g == 0:
                    bad = 1
    #        print "status",status[i], "\n"
            i = i + 1 #increment counter

    #    print " "
        if bad == 1:#if there is a closed clause
    #        print "bad \n"
    #        print "flipped? ", flipped[-1]
            if flipped[-1] == 0:#flip if you have not done so
                nextlit = literals[-1]^1
    #            print literals[-1]^1
                flipped[-1] = flipped[-1]+1
                literals.pop()
                h = 0
                for z in status:#subtract one from all status markers
                    if z > 0:
                        status[h] = z - 1
                    h = h + 1
    #            print "flipped \n"
                continue
            else:
                while flipped[-1] > 0:#if the top has already been flipped, start popping
                    poppedvar = literals.pop()#pop top
                    varstat[poppedvar>>1] = 0#reflect that this variable is unused
                    flipped.pop()#pop flipped
                    h = 0
                    for z in status:#subtract one from all status markers
                        if z > 0:
                            status[h] = z - 1
                        h = h + 1
                    if len(flipped) < 1:
    #                    print "wrong"
    #                    while 1:
    #                        d = 0
                        return "U"
                if flipped[-1] == 0:#flip if you have not done so
                    nextlit = literals[-1]^1
                    flipped[-1] = flipped[-1]+1
                    literals.pop()
                    h = 0
                    for z in status:#subtract one from all status markers
                        if z > 0:
                            status[h] = z - 1
                        h = h + 1
                    continue
    #    print "did I get here?"
        if 0 not in status: #if all statuses are full, return the literals that worked
    #        while 1:
    #           print "satisfied"
            return literals
        j = 0
        for r in status:
            if r == 0:
                for t in wffsrt[j]:
                    if varstat[t>>1] == 0:
                        nextlit = t
                        flipped.append(0)
                        break
                break
            j = j + 1
def main(argv):
    debug = argv[2] #set debug flag
    file_name = sys.argv[1] #read in file name
    allwffs = []
    f = open(file_name, 'r')#open file
    current = read_wff(f)
    print current
    if not current:
        f.close()
        return 0
    allwffs.append(current)
    while current:#read in the file until it has all been read
        current = read_wff(f)
        allwffs.append(current)
    allwffs.pop()
    f.close()
    n_sat = 0
    n_unsat = 0
    for awff in allwffs:
        start = time.time()
        answer = satis(awff)
        end = time.time()
        awff['time'] = (end - start) * 1000000
        if answer == "U":
            awff['answer'] = "U"
            n_unsat += 1
        else:
            awff['answer'] = "S"
            awff['assignment'] = answer
            n_sat += 1
        print create_output(awff)
    last_line = (sys.argv[1].split("."))[0] + ",avatar," + str(len(allwffs)) + ","
    last_line += str(n_sat) + "," + str(n_unsat) + "," + str(given) + "," + str(correct)
    print last_line
main(sys.argv)
