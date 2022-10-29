#########################################
###### Step 5 trong Training Phase ######
#########################################
from keywords_data.default_keywords import operator_keys
from gensim.models import Word2Vec

class ToVector:
    def __init__(self, *args, **kwargs):
        if "gadget_code" in kwargs:
            self.input_type = "gadget_code"
            self.token = self.process(kwargs["gadget_code"])
            
        elif "attention_code" in kwargs:
            self.input_type = "attention_code"
            self.token = self.process(kwargs["attention_code"])
        
        else:
            raise ValueError("Expects 'gadget_code' field or 'attention_code' field in args")
        
        self.vector_lenght = kwargs["vector_lenght"]
        self.backward_slices = 0
        self.forward_slices = 0
        
        self.words_embedding = None
        
    def process(self, data):
        tokennize_result = []
        for code in data:
            token_ = self.tokennize(code[self.input_type])
            tokennize_result.append(token_)
        return tokennize_result
        
    def tokennize(self, code):
        vectors = []
        for line in code:
            data = self.extract_line_to_vector(line)
            for i in data:
                vectors.append(i)
        return vectors
            
    def extract_line_to_vector(self, line):
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
    
    def train(self):
        model = Word2Vec(self.token, min_count = 1, vector_size = self.vector_lenght, sg = 1)
        self.words_embedding = model.wv
