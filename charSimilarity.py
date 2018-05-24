versionRCS='$Id: charSimilarity.py,v 1.11 2008/05/15 18:21:47 black Exp $'
#            *created  "Sat Feb  9 08:54:30 2008" *by "Paul E. Black"
versionMod=' *modified "Thu May 15 14:13:04 2008" *by "Paul E. Black"'

#----------------------------------------------------------------------------
#
# Return the basic visual similarity between two characters, like a and o,
# or between a pair of characters and a character, like rn and m.  Context
# adjustments, for instance, leading characters are more carefully 
# scrutinized than other characters and iiii is similar to iiiii, are
# handled elsewhere.
#
# Character similarity ranges from 0, completely different, to 1,
# visually indistinguishable (at least in some font).
#
# Similarity is based on typical fonts, like Courier and Times.  We ignore
# "fancy" fonts, like script - they're rarely used for URLs and have an
# entirely different set of similarities.
#
# Top-Level Domains are case insensitive.  To model this, all comparisons
# are done in lower case, even if it is the upper case version that causes
# confusion, like O and Q.
#
# Similarity is symmetric.  SIM_SCORE(X, Y) = SIM_SCORE(Y, X).
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

# Even though similarity is symmetric, the tables only have one of the pairs.
# That is, the tables don't have both X Y and Y X.

# single character similarity table
scsimtab = {
	('0', 'O'):	.9,
	('1', '7'):	.5,	# for European 1s
	('1', 'i'):	.9,	# in some fonts
	('1', 'l'):	1,	# identical in some fonts
	('2', 'Z'):	.2,
	('3', 'E'):	.1,	# maybe?
	('4', 'A'):	.1,	# in some fonts
	('4', 'H'):	.1,	# in some fonts
	('4', '9'):	.2,	# in some fonts
	('5', 'S'):	.2,
	('6', 'b'):	.3,
	('8', 'B'):	.3,
	('9', 'P'):	.1,	# maybe?
	('a', 'c'):	.2,
	('a', 'd'):	.2,
	('a', 'e'):	.2,
	('a', 'o'):	.3,
	('A', 'H'):	.1,
	('b', 'd'):	.2,
	#('B', 'D'):	.1, more similar as lower case, so ignore
	('b', 'h'):	.2,
	('B', 'E'):	.1,
	('B', 'P'):	.2,
	('B', 'R'):	.2,
	('c', 'e'):	.2,
	('c', 'o'):	.3,
	#('C', 'O'):	.2, more similar as lower case, so ignore
	('C', 'G'):	.2,
	('d', 'o'):	.2,
	('e', 'o'):	.2,
	('E', 'F'):	.2,
	('F', 'P'):	.1,
	('f', 't'):	.3,
	('g', 'q'):	.2,	# in some fonts
	('G', 'O'):	.1,
	('h', 'k'):	.1,
	#('H', 'K'):	.1, as similar as lower case, so ignore
	('h', 'n'):	.4,
	#('H', 'N'):	.2, more similar as lower case, so ignore
	('i', 'j'):	.5,	# in some fonts
	('I', 'l'):	1,	# identical in some fonts
	('K', 'X'):	.1,
	('m', 'n'):	.1,	# proportional fonts
	('n', 'r'):	.1,
	('o', 'p'):	.1,
	('O', 'Q'):	.4,
	('p', 'q'):	.1,
	('P', 'R'):	.2,
	('u', 'v'):	.1,
	('v', 'w'):	.1,
	('v', 'x'):	.1,
	('v', 'y'):	.2,
	# TO TEST SELF-TEST
	#('y', 'x'):	.1,
	('x', 'y'):	.1
}

# double character similarity table
dcsimtab = {
    ('cl', 'd'):	.4,	# in proportional fonts
    ('fl', 'f'):	.5,	# in fonts with ligatures
    ('mn', 'nm'):	.5,	# in proportional fonts
    ('nn', 'm'):	.5,	# in proportional fonts
    ('AA', 'M'):	.2,
    ('rn', 'm'):	1,	# I misread "warns" as "wams" once!
    ('VV', 'W'):	.8,	# in proportional fonts
}

#------------------------------------------------------------------------------
# initialize the similarity tables
#
# make sure there is a lower case version of every pair and
# check for table inconsistencies
#------------------------------------------------------------------------------

for (ch1, ch2) in scsimtab.keys():
    if ch1.isupper() or ch2.isupper():
        # make sure we don't override another entry
        if (ch1.lower(), ch2.lower()) in scsimtab:
            print 'Inconsistency: ('+ch1+', '+ch2+') to be inserted, but is already present as lower case.'
        scsimtab[(ch1.lower(), ch2.lower())] = scsimtab[(ch1, ch2)]

for (str1, str2) in dcsimtab.keys():
    # (python note: isupper() means is *all* upper case, so can't use it here)
    if not str1.islower() or not str2.islower():
        # make sure we don't override another entry
        if (str1.lower(), str2.lower()) in dcsimtab:
            print 'Inconsistency: ('+str1+', '+str2+') to be inserted, but is already present as lower case.'
        dcsimtab[(str1.lower(), str2.lower())] = dcsimtab[(str1, str2)]


#------------------------------------------------------------------------------
# how similar are two characters
#------------------------------------------------------------------------------

def characterSimilarity(ch1, ch2):
    """Rate the similarity of two characters."""

    # both parameters must be single characters
    assert(len(ch1) == 1)
    assert(len(ch2) == 1)

    # Characters must not be upper case
    assert(not ch1.isupper())
    assert(not ch2.isupper())

    # look up character pair in table
    if (ch1, ch2) in scsimtab:
	similarity = scsimtab[(ch1, ch2)]
    elif (ch2, ch1) in scsimtab:
	similarity = scsimtab[(ch2, ch1)]
    else:
	# character pair not in table, use default
	if ch1 == ch2:
	    similarity = 1
	else:
	    similarity = 0

    return similarity

def characterSimilarity_chkSym(str1, str2):
    """Check that characterSimilarity() is symmetric."""
    resultScore = characterSimilarity(str1, str2)
    reverseScore = characterSimilarity(str2, str1)
    if resultScore != reverseScore:
	print 'characterSimilarity failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, 'one way, and', \
				reverseScore, 'the other.'
    return resultScore

def characterSimilarity_chkPair(str1, str2, expectedScore):
    """Check that characterSimilarity() works in one instance."""
    resultScore = characterSimilarity_chkSym(str1.lower(), str2.lower())
    if resultScore != expectedScore:
	print 'characterSimilarity failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, \
				'instead of', str(expectedScore) + '.'

def characterSimilarity_selftest():
    """Built-in self test for characterSimilarity()."""
    print '    running self test for characterSimilarity() ...'
    #--------------------------------------------------------------------------
    # check consistency in the single character similarity table
    #--------------------------------------------------------------------------
    for (ch1, ch2) in scsimtab:
        # no pair should be in backwards
	if (ch2, ch1) in scsimtab:
	    print 'inconsistency in single char similarity table (scsimtab):'
	    print ' both ('+ch1+', '+ch2+') and ('+ch2+', '+ch1+') are present'
	# there should be lower case versions of every pair
	if not (ch1.lower(), ch2.lower()) in scsimtab:
	    print 'inconsistency in single char similarity table (scsimtab):'
	    print ' ('+ch1+', '+ch2+') present, but not ('\
				+ch1.lower()+', '+ch2.lower()+')'

    #--------------------------------------------------------------------------
    # some pairs of characters
    #--------------------------------------------------------------------------
    # Empty strings and None parameters are not handled
    #characterSimilarity_chkPair('', 'light on a hill', 0)
    characterSimilarity_chkPair('a', 'a', 1)
    characterSimilarity_chkPair('A', 'a', 1)
    characterSimilarity_chkPair('a', 'b', 0)
    characterSimilarity_chkPair('a', 'c', .2)
    characterSimilarity_chkPair('p', 'b', .2)
    characterSimilarity_chkPair('c', 'a', .2)
    characterSimilarity_chkPair('i', '1', .9)
    characterSimilarity_chkPair('l', '1', 1)
    characterSimilarity_chkPair('u', 'v', .1)
    characterSimilarity_chkPair('v', 'x', .1)
    characterSimilarity_chkPair('v', 'y', .2)

    #--------------------------------------------------------------------------
    print '    try all pairs of single characters'
    # for regression, I suppose - *I'm* not going to check each one manually
    #--------------------------------------------------------------------------

    # see RFC 1035 2.3.1 http://www.faqs.org/rfcs/rfc1035.html
    allowedCharacters = \
              'abcdefghijklmnopqrstuvwxyz0123456789-'
    
    for ch1 in allowedCharacters:
	for ch2 in allowedCharacters:
            resultScore = characterSimilarity_chkSym(ch1, ch2)
            print ch1, ch2, resultScore

    print '    self test for characterSimilarity() done.'

#------------------------------------------------------------------------------
# how similar are a digraph and a character or two digraphs
#------------------------------------------------------------------------------

def digraphSimilarity(dg1, dg2):
    """Rate the similarity of digraphs and characters."""

    #print dg1, dg2 # TEMP

    # both "digraphs" must be one or two characters
    assert(len(dg1) in [1, 2])
    assert(len(dg2) in [1, 2])
    # at least one of them must be two characters
    assert(len(dg1) == 2 or len(dg2) == 2)

    # Isn't it inefficient to convert to lower case over and over?
    # Yup, but speed isn't an issue, and it is clearer, more reliable,
    # and more flexible to do it in one place, here.
    dg1l = dg1.lower()
    dg2l = dg2.lower()

    # look up character pair in table
    if (dg1l, dg2l) in dcsimtab:
    	similarity = dcsimtab[(dg1l, dg2l)]
    elif (dg2l, dg1l) in dcsimtab:
    	similarity = dcsimtab[(dg2l, dg1l)]
    else:
	# pair not in table, use default
	if dg1l == dg2l:
	    similarity = 1
	else:
	    similarity = 0

    return similarity

def digraphSimilarity_chkSym(str1, str2):
    """Check that digraphSimilarity() is symmetric."""
    resultScore = digraphSimilarity(str1, str2)
    reverseScore = digraphSimilarity(str2, str1)
    if resultScore != reverseScore:
	print 'digraphSimilarity failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, 'one way, and', \
				reverseScore, 'the other.'
    return resultScore

def digraphSimilarity_chkPair(str1, str2, expectedScore):
    """Check that digraphSimilarity() works in one instance."""
    resultScore = digraphSimilarity_chkSym(str1, str2)
    if resultScore != expectedScore:
	print 'digraphSimilarity failed built-in test for', \
				str1, 'and', str2 + '.'
	print '    It returned', resultScore, \
				'instead of', str(expectedScore) + '.'

def digraphSimilarity_selftest():
    """Built-in self test for digraphSimilarity()."""
    print '    running self test for digraphSimilarity() ...'
    #--------------------------------------------------------------------------
    # check consistency in the digraph similarity table
    #--------------------------------------------------------------------------
    for (str1, str2) in dcsimtab:
        # no pair should be in backwards
	if (str2, str1) in dcsimtab:
	    print 'inconsistency in digraph similarity table (dcsimtab):'
	    print ' both ('+str1+', '+str2+') and ('+str2+', '+str1+') are present'
	# there should be lower case versions of every pair
	if not (str1.lower(), str2.lower()) in dcsimtab:
	    print 'inconsistency in digraph similarity table (dcsimtab):'
	    print ' ('+str1+', '+str2+') present, but not ('\
				+str1.lower()+', '+str2.lower()+')'

    #--------------------------------------------------------------------------
    # some pairs
    #--------------------------------------------------------------------------
    # Empty strings and None parameters are not handled
    #digraphSimilarity_chkPair('', 'light on a hill', 0)
    digraphSimilarity_chkPair('cl', 'd', .4)
    digraphSimilarity_chkPair('D', 'cl', .4)
    digraphSimilarity_chkPair('E', 'cl', 0)
    digraphSimilarity_chkPair('f', 'fL', .5)
    digraphSimilarity_chkPair('fl', 'F', .5)
    digraphSimilarity_chkPair('fm', 'FM', 1)
    digraphSimilarity_chkPair('MN', 'NM', .5)
    digraphSimilarity_chkPair('nm', 'mn', .5)
    digraphSimilarity_chkPair('nn', 'mn', 0)
    digraphSimilarity_chkPair('m', 'Nn', .5)
    digraphSimilarity_chkPair('nn', 'm', .5)
    digraphSimilarity_chkPair('nn', 'j', 0)
    digraphSimilarity_chkPair('Aa', 'M', .2)
    digraphSimilarity_chkPair('m', 'AA', .2)
    digraphSimilarity_chkPair('AA', 'AA', 1)
    digraphSimilarity_chkPair('m', 'Rn', 1)
    digraphSimilarity_chkPair('rn', 'm', 1)
    digraphSimilarity_chkPair('rP', 'm', 0)
    digraphSimilarity_chkPair('vv', 'w', .8)
    digraphSimilarity_chkPair('W', 'VV', .8)
    digraphSimilarity_chkPair('xb', 'JK', 0)

    # what WOULD a good semi-exhaustive test be??
    #--------------------------------------------------------------------------
    #print '    try all pairs of single characters'
    # for regression, I suppose - *I'm* not going to check each one manually
    #--------------------------------------------------------------------------

    # see RFC 1035 2.3.1 http://www.faqs.org/rfcs/rfc1035.html
    #allowedCharacters = \
    #         'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
    
    #for str1 in allowedCharacters:
    #	for str2 in allowedCharacters:
    #        resultScore = digraphSimilarity_chkSym(str1, str2)
    #        print str1, str2, resultScore

    print '    self test for digraphSimilarity() done.'

# end of $Source: /home/black/GTLD/RCS/charSimilarity.py,v $
