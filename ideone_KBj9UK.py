import fileinput, sys
import numpy
from collections import Counter
f = fileinput.input()

class Chest:
    pass

max_key = 200
T = int(f.readline())

def solve(chests, keys):
    keys = numpy.copy(keys)

    # first, check a quick necessary condition
    keys_across_universe = keys + sum(chest.inside for chest in chests)
    required = Counter(chest.lock for chest in chests)
    required = numpy.array([required[key] for key in range(max_key+1)])
    if any(required > keys_across_universe):
        return False
    
    explored = list()
    bad_prefixes = set()
           
    start = 0
    
    while True:
        #print >> sys.stderr, explored
        #print >> sys.stderr, keys
        
        for i in range(start, len(chests)):
            if i in explored:
                # already opened that chest
                continue
        
            chest = chests[i]
            if not keys[chest.lock]:
                # Don't have a key to open this chest.
                continue
                
            # Skip prefixes we discounted earlier.
            if frozenset(explored+[i]) in bad_prefixes:
                continue
                
            # Open the chest
            # print "Open chest %d" % i
            keys[chest.lock] -= 1
            explored.append(i)
            keys += chest.inside
            
            if len(explored) == len(chests):
                return explored

            start = 0
            break
        else:
            # There is no solution below us.
            if not explored:
                # The whole puzzle is impossible.
                # print >> sys.stderr, len(bad_prefixes)
                return False
            
            bad_prefixes.add(frozenset(explored))
            
            # Undo opening that last chest.           
            recent = explored.pop()
            # print "Undo opening chest %d" % recent
            chest = chests[recent]
            keys -= chest.inside  
            keys[chest.lock] += 1
            
            start = recent+1
        
            
        
    

for case in range(1,T+1):
    K, N = [int(x) for x in f.readline().split()]
    initial_keys = [int(x) for x in f.readline().split()]
    assert len(initial_keys) == K
    initial_keys = Counter(initial_keys)
    
    initial_keys = numpy.array([initial_keys[key] for key in range(max_key+1)])
    
    chests = list()
    
    for i in range(N):
        numbers = [int(x) for x in f.readline().split()]
        Ti = numbers[0]
        Ki = numbers[1]
        inside = numbers[2:]
        assert len(inside) == Ki
        inside = Counter(inside)
        inside = numpy.array([inside[key] for key in range(max_key+1)])
        assert inside[0] == 0
        
        chest = Chest()
        chest.lock = Ti
        chest.inside = inside
        chests.append(chest)
       
    solution = solve(chests, initial_keys)
    if solution:
        answer = " ".join(str(n+1) for n in solution)
    else:
        answer = "IMPOSSIBLE"
        
    print "Case #%d: %s" % (case, answer)