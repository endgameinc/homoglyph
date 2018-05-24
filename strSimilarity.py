versionRCS='$Id: strSimilarity.py,v 1.14 2008/05/15 18:21:23 black Exp $'
#            *created  "Sat Feb  9 08:54:30 2008" *by "Paul E. Black"
versionMod=' *modified "Thu May 15 14:12:24 2008" *by "Paul E. Black"'

#----------------------------------------------------------------------------
#
# Compute the visual similarity between two strings, which are Top-Level
# Domains (TLDs) or reserved words.
#
# String similarity ranges from 0, completely different, to 1,
# visually indistinguishable (at least in some font).
#
# See charSimilarity.py for more characteristics of the similarity function.
#
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties.  Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain.  This software is an
# experimental system.  NIST assumes no responsibility whatsoever for
# its use by other parties, and makes no guarantees, expressed or
# implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgment if this software is used.
#
# This software may be redistributed and/or modified freely provided
# that any modified versions bear some notice that they were modified.
#
# Paul E. Black  paul.black@nist.gov
#
#----------------------------------------------------------------------------

import charSimilarity

# Notes: similarity is not transitive.  SIM(X, Y) and SIM(Y, Z) does
#    NOT necessarily mean SIM(X, Z).

#----------------------------------------------------------------------------
#
#   Find the Levenshtein or edit distance between two strings,
#   including Damerau's refinement for transposting.  If characters
#   are visually similar, the substitution or transposition cost is
#   less than 1, the cost for an insertion or deletion.
#
# The following is not yet handled in the algorithm:
#
# Characters in the middle are confused more easily than characters at
#   the beginning or the end.
#
#----------------------------------------------------------------------------

# Return cost to add another repeated character to s to get t.  This
# is less than general insertion.
# SKIMP this only handles adding one more character, but who would
#    propose misssssippi and misssippi??
# SKIMP this does not handle "visual repetitions".  For instance,
#    .boom should be similar to .b000rn (oh vs. zero & m vs. rn)
def repetitionInsert(sl, i, tl, j):
    # The preceeding 2 chars in both strings must match and they are
    # repetitions of t[j].  Here is a passing case. The locations that
    # i and j point are shown.
    #        i j
    #        v |
    #  s   m M v
    #  t   M m m
    if i < 1 or j < 2 or sl[i-1:i+1] != tl[j-2:j] or tl[j-2:j] != tl[j]*2:
        return -1 # some condition not met - no repetition "discount"

    #print 'repetition:', sl[i-1:i+1], i, tl[j-2:j], j, tl[j]

    # how far back does the matching extend?
    back = 2
    mc = tl[j] # the matching character
    while back<=i and back<j and sl[i-back] == mc and tl[j-back-1] == mc:
        back += 1
    #print '      ', back, sl[i-back+1:i+1], i, tl[j-back:j], j, tl[j]

    # The scoring formula is a simple fit to scores that seem good to me
    #	Length	Cost
    #	  2	 .9
    #	  3 	 .5
    #	  4 	 .1
    #	 >4 	 0
    cost = max(0, 1.7 - 0.4*back)

    # SKIMP In a very complex function, we must return how far back the
    # match goes to access the right place in the cost matrix, d.  Strictly
    # speaking we replace, say, CC with CCC, not just insert a C.  Since the
    # preceeding "CC"s match at zero cost, this short cut shouldn't hurt.
    return cost

# possible improvements to the algorithm
#    from http://en.wikipedia.org/wiki/Levenshtein_distance)
#   We can adapt the algorithm to use less space, O(m) instead of O(mn),
# since it only requires that a few rows be stored at any one time.
#   By examining diagonals instead of rows, and by using lazy
# evaluation, we can find the Levenshtein distance in O(m (1 + d))
# time (where d is the Levenshtein distance), which is much faster
# than the regular dynamic programming algorithm if the distance is
# small.

# I derived levenshtein() from code originally accessed 8 Feb 2008 at
# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance 

traceLeven = 0

def levenshtein(s, t):
    """Find the Levenshtein (edit) distance between strings."""
    effInfinity = 9999999 # effectively infinity
    
    def updateCost(baseCost, oprCost, lowestCostSoFar, operation):
        (baseCostX, baseCostY) = baseCost
        if baseCostX >= 0 and baseCostY >= 0:
            newCost = d[baseCostX][baseCostY] + oprCost
            if newCost < lowestCostSoFar:
                if traceLeven: print newCost, oprCost, operation
                return newCost
        return lowestCostSoFar

    # TO TEST SELF-TEST
    # make sure symmetry self-test works
    # s = s+'s'
    len_s = len(s)
    len_t = len(t)
    sl = s.lower() # do all comparisons lower case
    tl = t.lower()

    # CAUTION: HARDCODED INSERTION COST FOR EACH LOCATION
    d = [range(len_t+1)]
    d += [[i] for i in range(1, len_s+1)]
    if traceLeven: print s, t, d # diagnostic
    for i in xrange(0, len_s):
        for j in xrange(0, len_t):
            minCost = effInfinity
            
	    # "delete" or "insert" is in terms of changing s into t

            # delete
            minCost = updateCost((i, j+1), 1, minCost, 'd '+s[i])
                
            # insert
            minCost = updateCost((i+1, j), 1, minCost, 'i '+t[j])

            # insert after repetition
            repiCost = repetitionInsert(sl, i, tl, j)
            if repiCost >= 0:
                minCost = updateCost((i+1, j), repiCost, minCost, 'ri '+t[j])

            # delete after repetition
            repdCost = repetitionInsert(tl, j, sl, i)
            if repdCost >= 0:
                minCost = updateCost((i, j+1), repdCost, minCost, 'rd '+s[i])

            # substite s[i] by t[j] - 0 cost if identical
            subsCost = 1 - charSimilarity.characterSimilarity(sl[i], tl[j])
            minCost = updateCost((i, j), subsCost, minCost,'s '+s[i]+'->'+t[j])

            # compute total costs of 2 for 1, 1 for 2, or 2 for 2 substitution
            if i > 0:
                # cost of substituting s[i-1:i+1] by t[j]
                subs21Cost = \
                         1-charSimilarity.digraphSimilarity(sl[i-1:i+1],tl[j])
                if subs21Cost == 1: subs21Cost = 2 # substitute TWO characters
                minCost = updateCost((i-1, j), subs21Cost, minCost, 's21')
            if j > 0:
                # cost of substituting s[i] by t[j-1:j+1]
                subs12Cost = \
                         1-charSimilarity.digraphSimilarity(sl[i],tl[j-1:j+1])
                if subs12Cost == 1: subs12Cost = 2 # substitute TWO characters
                minCost = updateCost((i, j-1), subs12Cost, minCost, 's12')
            if i > 0 and j > 0:
                # cost of substituting s[i-1:i+1] by t[j-1:j+1]
                subs22Cost = \
                    1-charSimilarity.digraphSimilarity(sl[i-1:i+1],tl[j-1:j+1])
                if subs22Cost == 1: subs22Cost = 2 # substitute TWO characters
                minCost = updateCost((i-1, j-1), subs22Cost, minCost, 's22')

                # cost of transposing s[i-1] and s[i] to get t[j-1] and t[j]
                if sl[i-1] == tl[j] and sl[i] == tl[j-1]:
		    transpCost = \
                        1 - charSimilarity.characterSimilarity(sl[i], tl[j])
		    minCost = updateCost((i-1, j-1), transpCost, minCost, 't')
            d[i+1].append(minCost)
            if traceLeven: print d #diagnostic
    if traceLeven: print d #diagnostic
    return d[len_s][len_t]

# floats are rarely exactly the same. this allows for a range
def fEqual(f1, f2):
    """Return True if floats passed are nearly equal."""
    epsilon = .0000001
    if abs(f1 - f2) < epsilon:
        return True
    return False

def levenshtein_chkSym(str1, str2):
    """Check that levenshtein() is symmetric."""
    resultScore = levenshtein(str1, str2)
    reverseScore = levenshtein(str2, str1)
    if resultScore != reverseScore:
	print 'levenshtein failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, 'one way, and', \
				reverseScore, 'the other.'
    return resultScore

def levenshtein_chkPair(str1, str2, expectedScore):
    """Check that levenshtein() works in one instance."""
    resultScore = levenshtein_chkSym(str1, str2)
    # check that it returned the expected score
    if not fEqual(resultScore, expectedScore):
	print 'levenshtein() failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, \
				'instead of', str(expectedScore) + '.'

def levenshtein_selftest():
    """Built-in self test levenshtein()."""
    print '    running self test for levenshtein() ...'
    # check degenerate cases
    levenshtein_chkPair('', '', 0)
    levenshtein_chkPair('a', '', 1)
    levenshtein_chkPair('bc', '', 2)
    # check simple cases
    levenshtein_chkPair('G', 'G', 0)   # same character
    levenshtein_chkPair('H', 'h', 0)   # upper case vs. lower case
    levenshtein_chkPair('i', 'qI', 1)  # insertion before
    levenshtein_chkPair('J', 'Jd', 1)  # insertion after
    levenshtein_chkPair('K', 'mk-', 2) # insertion before and after
    levenshtein_chkPair('s', 'x', 1)   # substitution
    levenshtein_chkPair('lrQ', 'l4q', 1) # embedded substitution
    # check similar single character substitutions
    levenshtein_chkPair('T1', 'tl', 0)
    levenshtein_chkPair('uh', 'vH', .9)
    levenshtein_chkPair('Scar', 'Soar', .7)
    levenshtein_chkPair('labsRUs', 'ladsRUs', .8)
    # check similar double character substitutions
    levenshtein_chkPair('f', 'fl', .5)
    levenshtein_chkPair('Clock', 'Dock', .6) # lower case looks similar
    levenshtein_chkPair('WN', 'vvn', .2) # at beginning
    levenshtein_chkPair('mn', 'mn', 0)
    levenshtein_chkPair('Mn', 'nm', .5)
    levenshtein_chkPair('xmn', 'xnm', .5) # at end
    levenshtein_chkPair('m', 'NN', .5)
    levenshtein_chkPair('AAf', 'mFL', 1.3) # two substitutions
    levenshtein_chkPair('wams', 'warns', 0) # embedded
    # check transposition
    levenshtein_chkPair('often', 'otfen', .7)
    levenshtein_chkPair('cheif', 'chief', 1)
    levenshtein_chkPair('Pterodactyl', 'Tperodactyl', 1) # mixed case
    # check repetition insert
    levenshtein_chkPair('Mm', 'mmM', .9) # minimal, longer on right
    levenshtein_chkPair('XIIII', 'XIII', .5) # 4 vs. 3, longer on left
    levenshtein_chkPair('aaaah', 'aaaaah', .1) # 4 vs. 5, at start
    levenshtein_chkPair('MiSSsssipPpi', 'MisSSssSippi', .9)
    # other checks
    levenshtein_chkPair('xw', '5t', 2)
    levenshtein_chkPair('w', 'dd', 2)
    levenshtein_chkPair('', 'We-the-People-of-the-United-States-in-Order-to-form-a-more-perfect-Union-establish-Justice-insure-domestic-Tranquility-provide-for-the-common-defence-promote-the-general-Welfare-and-secure-the-Blessings-of-Liberty-to-ourselves-and-our-Posterity-do-ordain-and-establish-this-Constitution-for-the-United-States-of-America', 319) # long word
    levenshtein_chkPair('aerometeorograph','floccinaucinihilipilification',26.1)
    #levenshtein_chkPair('', '', )
    print '    self test for levenshtein() done.'


#----------------------------------------------------------------------------
#
#   Compute how confusable or visually similar two strings are.  Range
#   is [0, 1] where 1 is visually identical and 0 means completely
#   different.
#
#----------------------------------------------------------------------------

def howConfusableAre(str1, str2):
    """Rate the visible similarity of the strings.

    Rating is 0 to 1 inclusive, where 1 means visually indistinguishable."""

    # None parameters not handled

    # TO TEST SELF-TEST
    # does the symmetry self-check really catch an error?
    #if str1 == 'a':
    #    return .777

    # Begin with a Levenshtein distance between the strings.
    # Substitution of visually similar characters "costs" less than
    # one insertion, deletion, or substitution
    levDist = 0.0 + levenshtein(str1, str2)

    # Normalize to [0, 1] and account for longer words being more
    # confusable than shorter words with the same Levenshtein distance
    minlen = min(len(str1), len(str2))
    maxlen = max(len(str1), len(str2))
    lendiff = abs(len(str1) - len(str2))
    # SKIMP the maxlen==0 test is approximate.  Strictly, we should
    # ask if the values used in the scoring would be n/0.  But I don't
    # want to be changing this test all the time while the scoring fn
    # is changing.
    if maxlen == 0:
	score = 1 # null strings are identical
    else:
	score = (maxlen - levDist)/(maxlen + 3*levDist + lendiff*levDist)
        #print score, minlen, levDist, levDist**2

    # make SURE it is normalized
    if not (0 <= score and score <= 1):
        print '**ERROR: NON-NORMAL SCORE:', score, 'for', str1, str2
    assert(0 <= score and score <= 1)
    
    return score

def howConfusableAre_chkSym(str1, str2):
    """Check that howConfusableAre() is symmetric."""
    resultScore = howConfusableAre(str1, str2)
    reverseScore = howConfusableAre(str2, str1)
    if resultScore != reverseScore:
	print 'howConfusableAre failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, 'one way, and', \
				reverseScore, 'the other.'
    return resultScore

# scores only need 1 (or 2) decimal places of accuracy
def closeEnough(f1, f2):
    """Return True if floats passed are nearly equal."""
    epsilon = .01
    if abs(f1 - f2) < epsilon:
        return True
    return False

def howConfusableAre_chkPair(str1, str2, expectedScore):
    """Check that howConfusableAre() works in one instance."""
    resultScore = howConfusableAre_chkSym(str1, str2)
    if not closeEnough(resultScore, expectedScore):
	print 'howConfusableAre failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, \
				'instead of', str(expectedScore) + '.'

def howConfusableAre_selftest():
    """Built-in self test for howConfusableAre()."""
    charSimilarity.characterSimilarity_selftest()
    charSimilarity.digraphSimilarity_selftest()
    levenshtein_selftest()
    print '    running self test for howConfusableAre() ...'
    howConfusableAre_chkPair('', '', 1)
    howConfusableAre_chkPair('', '2', 0)
    howConfusableAre_chkPair('y', 'Y', 1)
    howConfusableAre_chkPair('a', 'ab', .17)
    howConfusableAre_chkPair('Corn', 'Com', 1)
    howConfusableAre_chkPair('biz', 'bz', .29)
    howConfusableAre_chkPair('evample', 'example', .63)
    howConfusableAre_chkPair('exomple', 'example', .69)
    howConfusableAre_chkPair('exarnple', 'example', 1)
    howConfusableAre_chkPair('examqle', 'example', .63)
    howConfusableAre_chkPair('examp1e', 'example', 1)
    howConfusableAre_chkPair('exampl', 'example', .55)
    howConfusableAre_chkPair('examplo', 'example', .66)
    howConfusableAre_chkPair('z', 'zoology', .016)
    print '    self test for howConfusableAre() done.'

# end of $Source: /home/black/GTLD/RCS/strSimilarity.py,v $
