import sys
import os
import subprocess
import re

num_args = len(sys.argv)

if num_args != 2:
    print """
Usage: codedelta <gitpath..>
"""
    sys.exit(2);
        
gitpath = sys.argv[1]
os.chdir(gitpath)

# Map of author to number of inserted and deleted lines of code.
authorToCode = {} 

# Get the list of authors.
authors = subprocess.Popen("git log --format='%aN' | sort -u", 
                            shell=True, stdout=subprocess.PIPE)
authorList = authors.communicate()[0].split('\n')

# For each author, compute his/her number of lines of code.
# Assumed that authorList is ordered and each element is unique.
for author in authorList:
    if len(author) == 0:
        continue
    command = 'git log --since=2.weeks --author=\"' + author + '\" --pretty=tformat: --numstat'

    stats = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    statLines = stats.communicate()[0].split('\n')
    
    authorToCode[author] = {'insertions': 0, 'deletions': 0}

    for line in statLines:
        if len(line) == 0:
            continue
        elements = line.split()
        
        try: 
            insertions = int(elements[0])
            deletions = int(elements[1])
        except ValueError:
            continue # Punt if there's a parse error.
 
        authorToCode[author]['insertions'] += insertions
        authorToCode[author]['deletions'] += deletions
        
    total = authorToCode[author]['insertions'] + authorToCode[author]['deletions']
    print '{} {} {} {}'.format(author, total, insertions, deletions)
    