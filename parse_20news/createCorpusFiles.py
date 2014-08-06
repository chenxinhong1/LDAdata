#This script slip corpus into 15 70 15 percentage for DEV, TRAIN, TEST
import sys
import random
import re
import os
import glob
import math
import string

#create raw content for text
def composeContent(infile):
	index=0
	lines=0
	doc=""
	with open(infile) as file:
		for line in file:
			if lines==0:
				x = line.rstrip().find("Lines:")
				if x!=-1:
					try:
						lines=(int)(line.rstrip()[x:].split(" ")[1])
					except ValueError:
						print line.rstrip(), infile
						continue
			else:
				if index==0:
					doc=line.rstrip()
					index+=1
				elif index<lines:
					doc =doc+" "+line.rstrip()
					index+=1
				else:
					break
	return re.sub(" +"," ",doc.lower())			

if len(sys.argv)<3:
	print "Usage: train label file, dev label file, test label file"
	sys.exit()

#open label files and move the content of each file
train_labels_file =sys.argv[1]
dev_labels_file = sys.argv[2]
test_labels_file =sys.argv[3]
devLabels =dict()
testLabels=dict()
trainLabels=dict()

with open(train_labels_file) as file:
	for line in file:
		trainLabels[line.rstrip()]=True

with open(dev_labels_file) as file:
	for line in file:
		devLabels[line.rstrip()] =True

with open(test_labels_file) as file:
	for line in file:
		testLabels[line.rstrip()]=True

train_raw=open('20news.train.raw','w')
dev_raw=open('20news.dev.raw','w')
test_raw=open('20news.test.raw','w')

for fileLocation in glob.iglob(os.path.join('20news-bydate-test','*','*')):
	if fileLocation in devLabels:
		dev_raw.write(composeContent(fileLocation)+"\n")
	elif fileLocation in testLabels:
		test_raw.write(composeContent(fileLocation)+"\n")
	else:
		print fileLocation +" is not in the dev or test labels"

for fileLocation in glob.iglob(os.path.join('20news-bydate-train','*','*')):
	if fileLocation in trainLabels:
		train_raw.write(composeContent(fileLocation)+"\n")
	else:
		print fileLocation +" is not in the train labels"

test_raw.close()
dev_raw.close()
train_raw.close()



