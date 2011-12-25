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
	#print command
	# for each author, get their stats
	stats = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	statLines = stats.communicate()[0].split('\n')
	print author
	for line in statLines:
		if len (line) == 0:
			continue
		elements = line.split()
		#print line
		#print "insertions: " + elements[0]
		#print "deletions: " + elements[1]
		
		if author in authorToCode: 
			print "adding"
			authorToCode[author]['insertions'] += int(elements[0])
			authorToCode[author]['deletions'] += int(elements[1])
		else:
			print "creating new"
			codeDelta = {'insertions': int(elements[0]), 'deletions': int(elements[1])}
			authorToCode[author] = codeDelta
print authorToCode
	