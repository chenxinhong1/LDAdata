import sys
import string
if len(sys.argv)<1:
	print "Please provide a dictionary file (line by line)"
	sys.exit()

input_file = sys.argv[1]

output_file = input_file+".oneline"
out = open(output_file,'w')

vocab = list()
with open(input_file) as file:
	for word in file:
		vocab.append(word.rstrip())

out.write(' '.join(vocab)+"\n")
out.close()	

