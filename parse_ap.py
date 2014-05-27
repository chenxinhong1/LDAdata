import nltk;
import sys;

# this method reads in the data from raw ap data and parse to the mr lda format
def parse_ap(input_path, output_path):
    from nltk.corpus import stopwords
    stop = stopwords.words('english')

    from nltk.tokenize.punkt import PunktWordTokenizer 
    tokenizer = PunktWordTokenizer()

    from nltk.stem.porter import PorterStemmer
    stemmer = PorterStemmer();
    
    from string import ascii_lowercase
    
    doc_title = "";
    doc_content = [];
    doc_count = 0;
      
    input_file_stream = open(input_path, 'r');
    output_file_stream = open(output_path, 'w');
    for line in input_file_stream:
        line = line.strip().lower();
        
        if line=="<text>" or line=="</text>":
            continue;
        
        if line=="<doc>":
            continue;
        
        if line=="</doc>":
            output_file_stream.write("%s\t%s\n" % (doc_title, " ".join(doc_content)));
            doc_count += 1;
            if doc_count%1000==0:
                print("successfully parsed %d documents" % (doc_count));
            continue;
         
        if line.startswith("<docno>"):
            line = line.lstrip("<docno>");
            line = line.rstrip("</docno>");
            doc_title = line.strip();
            continue;
            
        #doc_content = [stemmer.stem(x) for x in tokenizer.tokenize(line) if (min(y in ascii_lowercase for y in x))];
        doc_tokens = [x for x in tokenizer.tokenize(line) if (min(y in ascii_lowercase for y in x))];
        doc_content = [stemmer.stem(x) for x in doc_tokens if x not in stop];

if __name__ == "__main__":
    input_path = sys.argv[1];
    output_path = sys.argv[2];
    parse_ap(input_path, output_path);
