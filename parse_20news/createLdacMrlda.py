#This script process 20news group
import sys
import random
import re
import os
import glob
import math
import string
#from nltk.tokenize.punkt import PunktWordTokenizer
#tokenizer =PunktWordTokenizer()
#from nltk.stem.porter import PorterStemmer
#stemmer = PorterStemmer()
#from string import ascii_lowercase


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

#function to print to fileName the corpus with given vocabulary
def createLdacFile(vocab, corpus,fileName,statFileName, rawFileName, mrldaFileName):
        file =open(fileName,'w')
        stat_file =open(statFileName,'w')
	raw_file =open(rawFileName,'w')
	mrlda_file =open(mrldaFileName,'w')
        stat_file.write("labels for "+fileName+"\n")
	stat_file.write("these labels are in order with the corresponding ldac file\n")
        docIndex=0
        for doc_label in corpus:
		doc = corpus[doc_label]
		uniqWord = getUniqCountInVocab(doc, vocab)
		if uniqWord > 2:
                	words =doc.split()
			mrldaDoc =list()
	                doc_dict =dict() #contains index of word and frequency
			proceed =0
                	for word in words:
                        	if word.strip() in vocab:
					mrldaDoc.append(word.strip())
                                	tmpIndex =vocab[word.strip()]
                                	if tmpIndex in doc_dict:
                                        	doc_dict[tmpIndex] +=1
                                	else:
                                        	doc_dict[tmpIndex]=1
			aDoc=str(uniqWord)
                        for i in sorted(doc_dict.iterkeys()):
                               	aDoc+=" "+str(i)+":"+str(doc_dict[i])
                        file.write(aDoc+"\n")
                        stat_file.write(str(docIndex)+"\t"+doc_label+"\n")
                        #print raw file
			raw_file.write(doc+"\n")
			#print mrlda file 
			mrldaText =" ".join(mrldaDoc)
			mrlda_file.write(doc_label+"\t"+mrldaText+"\n")
			docIndex+=1
		else:
			print "discarding "+ doc_label
        file.close()
        stat_file.close()
	raw_file.close()
	mrlda_file.close()

def getUniqCountInVocab(text, dictionary):
        tmp =dict()
        words = text.split()
        for word in words:
                if word.strip() in dictionary:
                        tmp[word.strip()] =True
        return len(tmp)


#count uniuq word in text
def getUniqCount(text):
	tmp =dict()
	words =text.split()
	for word in words:
		tmp[word.strip()] =True
	return len(tmp)


if len(sys.argv)<5:
	print "Usage: train label file, dev label file, test label file, min frequency, max frequency"
	sys.exit()

#regular exp to remove non-alphanumeric
alphabetReg ="[a-z]+$"

#open label files and move the content of each file
train_labels_file =sys.argv[1]
dev_labels_file = sys.argv[2]
test_labels_file =sys.argv[3]
min_freq = int(sys.argv[4])
max_freq = int(sys.argv[5])

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

#create corpus
train_corpus=dict()
dev_corpus=dict()
test_corpus=dict()

for fileLocation in glob.iglob(os.path.join('20news-bydate-test','*','*')):
	if fileLocation in devLabels:
		dev_corpus[fileLocation] = composeContent(fileLocation)
	elif fileLocation in testLabels:
		test_corpus[fileLocation] = composeContent(fileLocation)
	else:
		print "IGNORED ",fileLocation

for fileLocation in glob.iglob(os.path.join('20news-bydate-train','*','*')):
	if fileLocation in trainLabels:
		train_corpus[fileLocation] = composeContent(fileLocation)
	else:
		print "IGNORED ",fileLocation

#create dictionary based on train_corpus
vocab=dict()

for loc in train_corpus:
	doc =train_corpus[loc]
	if getUniqCount(doc) >2: #only count doc with more than 2 unique words 
		words = train_corpus[loc].split()
		for word in words:
                	tmpWord =word.strip()
                	if len(tmpWord)>2 and bool(re.match(alphabetReg,tmpWord)):#only keep word in this format/change this if needed
                        	if tmpWord in vocab:
                                	vocab[tmpWord]+=1
				else:
					vocab[tmpWord]=1
#remove words with frquencey <freq_threshold
tmp_vocab=dict()
for w in vocab:
	if vocab[w] >=min_freq and vocab[w] <=max_freq:
		tmp_vocab[w] = True


#print vocab to file and create sorted dict
corpus_name ="20news"
vocab_file =open(corpus_name+".vocab.txt","w")
train_vocab = dict()
index = 0
for term in sorted(tmp_vocab.iterkeys()):
	train_vocab[term] = index
	vocab_file.write(term+"\n")
	index+=1
vocab_file.close()

#create train, dev, test file according to the dict
createLdacFile(train_vocab, train_corpus,corpus_name+".ldac.train",corpus_name+".stat.train", corpus_name+".raw.train", corpus_name+".mrlda.train")
createLdacFile(train_vocab, test_corpus, corpus_name+".ldac.test",corpus_name+".stat.test", corpus_name+".raw.test", corpus_name+".mrlda.test")
createLdacFile(train_vocab, dev_corpus, corpus_name+".ldac.dev",corpus_name+".stat.dev", corpus_name+".raw.dev", corpus_name+".mrlda.dev")

