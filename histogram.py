#!/usr/bin/python3
import os
import re
import sys

''' The words contained in the list file must be separated by blanks. '''

# Check argument list first
if (len(sys.argv)) < 3:
    print ('Please specify directory for the Folder and for the list.')
    print ('eg. "./histogram.py Folder list.txt"')
    exit()

# Files variables
myFolder = sys.argv[1] #'Folder'
mylist = sys.argv[2] #'list.txt'
mytextfile = ''
mytextfiles = []

WORDSINLIST = []    # This variable will hold all words in rfList
APPEARANCE = []    # This variable will hold the number of appearance for all words in rfList

# Asuming myList is a small file
with open(mylist, 'r') as rfList:
    lines = list(rfList) # read all lines at once
rfList.close()

# write all filenames into the mytextfiles list
for root, dirs, files in os.walk(myFolder):
    for filename in files:
        mytextfiles.append(filename)

def testmatch(expression1, expression2, ignorecase):
    my_regex = r"\b"+re.escape(expression1)+r"\b" # set all match criteria here

    if(ignorecase):
        result = re.match(my_regex, expression2, re.IGNORECASE)
    else:
        result = re.match(my_regex, expression2)

    if  (result):
        return True
    else:
        return False

# Get a single word out of a line
def getword(inputline, index):
    if inputline == "":
        return ""
    regex = re.compile(r'(\S+)') # Include all elements with one or more char that are not a blank.
    words = regex.findall(inputline)
    if index >= len(words) or index < 0:
        return ""
    return words[index]

def parselist():
    # Parse through all lines
    for linenum in range(0, (len(lines))):
        # Parse through all words in lines[linenum]
        wordfromlist ='-'
        i = 0
        while wordfromlist != '':
            wordfromlist = getword(lines[linenum],i)
            if wordfromlist != '':
                # All words in List appear in this line
                WORDSINLIST.append(wordfromlist) # Fill array
                APPEARANCE.append(0) # Initialize APPEARANCE array
            i = i + 1

parselist()

print('...')
print('')

# Parse words through all Textfiles
for i in range(0, (len(mytextfiles))):
    mytextfile = myFolder+'/'+mytextfiles[i]
    with open(mytextfile, 'r') as rfText:
        for linerfText in rfText:
            # All lines within all files in Folder go through this position in code
            wordfromText ='-'
            j = 0
            while wordfromText != '':
                wordfromText = getword(linerfText,j)
                if wordfromText != '':
                    # All words in all Textfiles are processed in this line
                    for m in range(0, (len(WORDSINLIST) - 1)):
                        if testmatch(WORDSINLIST[m], wordfromText, True): # Check all List words for matches
                            APPEARANCE[m] = APPEARANCE[m] + 1
                j = j + 1
    rfText.close()

#Writing Histogram output
print('Folder: ', myFolder,'   ','List: ',mylist)
print('')
print('Searched Files:')
for q in range(0, (len(mytextfiles))):
    print('File',(q+1),mytextfiles[q])
print('')
print('*********************   HISTOGRAM   *************************')
print('                                                             ')
print('     Words in List           Appearance in all Documents     ')
print('                                                             ')
for k in range(0, (len(WORDSINLIST) - 1)):
    print('{:>12s}{:^64d}'.format(WORDSINLIST[k],APPEARANCE[k]))
    print('')
print('*******************  END of HISTOGRAM   *********************')
print('')
#EOF
