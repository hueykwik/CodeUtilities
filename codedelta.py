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

#author->dict(ins, removed)
authorToCode = {}

# get the list of authors
authors = subprocess.Popen("git log --format='%aN' | sort -u", shell=True, stdout=subprocess.PIPE)
authorList = authors.communicate()[0].split('\n')
for author in authorList:
	if len(author) == 0:
		continue
	command = 'git log --author=\"' +author+ '\" --pretty=tformat: --numstat'

	# for each author, get their stats
	stats = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	statLines = stats.communicate()[0].split('\n')
	
	for line in statLines:
		if len (line) == 0:
			continue
		elements = line.split()
		
		try: 
			insertions = int(elements[0])
			deletions = int(elements[1])
		except ValueError:
			# if it's not an integer, just punt
			continue

		if author in authorToCode: 
			authorToCode[author]['insertions'] += insertions
			authorToCode[author]['deletions'] += deletions
		else:
			codeDelta = {'insertions': insertions, 'deletions': deletions}
			authorToCode[author] = codeDelta
	total = authorToCode[author]['insertions'] + authorToCode[author]['deletions']
	print '{} {} {} {}'.format(author, total, insertions, deletions)
	