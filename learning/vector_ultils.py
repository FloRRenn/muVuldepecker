#########################################
###### Step 5 trong Training Phase ######
#########################################
from keywords_data.default_keywords import operator_keys
from gadget_ultils import function_regex

from gensim.models import Word2Vec
from pandas import DataFrame
import numpy as np
        
class Vector:
    def __init__(self, gadget_codes_map):
        self.vector_size = 100
        self.gadget_codes_map = gadget_codes_map
        
        self.tokens = self.to_token(gadget_codes_map)
        self.word_embedding = self.train_word2vec(self.tokens)
        
    def tokenize(self, line):
        pos = 0
        res = []
        keyword = ""
        
        def add(keyword, operator, pos, offset):
            if keyword:
                res.append(keyword)
                
            if operator:
                res.append(operator)
            
            keyword = ""
            pos += offset
            return keyword, pos
        
        while (pos < len(line)):
            # ignore whitespace
            if line[pos] == " ":
                offset = 1
                keyword, pos = add(keyword, None, pos, offset)
            
            # if it is <<=, >>=
            elif len({line[pos:pos + 3]}.difference(operator_keys)) == 0:
                offset = 3
                keyword, pos = add(keyword, line[pos:pos + offset], pos, offset)
            
            # if it is ++, --, +=, ||, &&,.....
            elif len({line[pos:pos + 2]}.difference(operator_keys)) == 0:
                offset = 2
                keyword, pos = add(keyword, line[pos:pos + offset], pos, offset)
            
            # if it is +, -, *, /,..... 
            elif len({line[pos]}.difference(operator_keys)) == 0:
                offset = 1
                keyword, pos = add(keyword, line[pos:pos + offset], pos, offset)
            
            # if it is a word   
            else:
                keyword += line[pos]
                pos += 1
        
        return res
    
    def add_token(self, code):
        tokenized = []
        backwards_slice = False
        
        for line in code:
            tokens = self.tokenize(line)
            tokenized += tokens
            
            if len(list(filter(function_regex.match, tokens))) > 0:
                backwards_slice = True
        
        return tokenized, backwards_slice
    
    def vectorize(self, gadget):
        tokenized_gadget, backwards_slice = self.add_token(gadget)
        vectors = np.zeros(shape = (50, self.vector_size))
        
        if backwards_slice:
            for i in range(min(len(tokenized_gadget), 50)):
                vectors[50 - 1 - i] = self.word_embedding[tokenized_gadget[len(tokenized_gadget) - 1 - i]]
        else:
            for i in range(min(len(tokenized_gadget), 50)):
                vectors[i] = self.word_embedding[tokenized_gadget[i]]
                
        return vectors
    
    def to_token(self, gadget_codes_map):
        tokenizer = []
        for data in gadget_codes_map:
            tokenized_gadget, _ = self.add_token(data['gadget_code'])
            tokenizer.append(tokenized_gadget)
            
        return tokenizer
        
    def to_dataframe(self):
        vectors = []
        
        for data in self.gadget_codes_map:
            vec = self.vectorize(data["gadget_code"])
            row = {"vector" : vec, "val" : data["exit_code"]}
            vectors.append(row)
        
        df = DataFrame(vectors)
        return df
    
    def train_word2vec(self, tokens):
        model = Word2Vec(tokens, min_count = 1, vector_size = self.vector_size, sg = 1)
        return model.wv
    
