#!/usr/bin/evn python
# -*- coding: utf-8 -*-

import operator
def readData(fileName):
	f = open(fileName, 'r')
	lines = f.readlines()
	for line in lines:
		line = line.replace("\n","")
		if word.has_key(line):
			word[line] = word[line] + 1
		else:
			word[line] = 1
		#print(line)
	f.close()

word = {}

for i in range(1,4):
	readData("data0" + str(i) + ".txt")


f = open("output.txt",'w')
for line in word:
	print(line , word[line])
	#print (line)
	#f.write(line + " " + str(word[line]) + "\n")
f.close()


sorted_cnt = sorted(word.items(), key=operator.itemgetter(1), reverse=True)

f = open("sorted_output.txt",'w')
for line in sorted_cnt[0:10]:
	#print(line , sorted_cnt[line])
	print(line[0], line[1])
	f.write(line[0] + " " + str(line[1])+ "\n")
	#f.write(line)
	#f.write(line + " " + str(sorted_cnt[line]) + "\n")
f.close()

print (sorted_cnt[0:10])