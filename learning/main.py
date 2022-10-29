from sklearn import ensemble
from gadget_ultils import extract_modify_gadget_code
from vector_ultils import ToVector
            
if __name__ == '__main__':
    filename = "./dataset/test.txt"
    
    gadget_codes_map = extract_modify_gadget_code(filename)
    vector_model = ToVector(gadget_code = gadget_codes_map, vector_lenght = 100)
    print(vector_model.token)
    #vector_model.train()