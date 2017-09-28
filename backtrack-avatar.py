import sys
import time
def read_wff (f): # reads in file of wffs
    wff = {}
    line = f.readline().strip() # reads first line
    if not line: # if line empty return nothing
        return
    line = line.split(" ")
    wff['problem'] = line[1] # 2nd element is problem number
    wff['maxLiterals'] = line[2]#3rd is maximum number of literals
    wff['testSat'] = line[3]#4th is the solution
    line = f.readline().strip()#next line
    line = line.split(" ")
    wff['nVar'] = int(line[2])#total number of variables
    wff['nClause'] = line[3]#number of clauses
    wff['clauses'] = []# start lists of clauses, variables, and lits
    wff['vars'] = []
    wff['lits'] = []
    for i in range(0, int(wff['nClause'])):#loop through each clause
        line = f.readline().strip()#each line contains a clause
        line = line.split(",")
        currentClause = []
        for lit in line:
            lit = int(lit)
            if lit < 0:#if negative/negated, multiply by 2 and add 1
                currentLit = 2 * abs(lit) + 1
            else:#if not negated, multiply by 2
                currentLit = 2 * abs(lit)
            currentClause.append(currentLit)#add lit to clause list
            if currentLit not in wff['lits']:#add lit if needed
                wff['lits'].append(currentLit)
            if abs(lit) not in wff['vars']:#add var if needed
                wff['vars'].append(abs(lit))
        wff['clauses'].append(currentClause)#add current clause list to overall list
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
                        return "ns"
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
    f.close()
    for awff in allwffs:
        print awff['problem'],",",awff['nVar'],",",awff['nClause'],",",awff['']
        answer = satis(awff)
        if answer == "ns":
            print 'U\t'
        else:
            print 'S\t'
        print awff['testSat']

main(sys.argv)
