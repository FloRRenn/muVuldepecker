from gadget_ultils import extract_modify_gadget_code
from vector_ultils import Vector
from blstm import BLSTM
import time
            
if __name__ == '__main__':
    filename = "./dataset/gadget_code/cwe119_cgd.txt"
    
    starttime = time.time()
    
    print("1. Generating gadget code: ")
    gadget_codes_map = extract_modify_gadget_code(filename)
    
    print("2. Generating dataframe: ")
    vector_model = Vector(gadget_codes_map)
    dataframe = vector_model.to_dataframe()
    
    print("3. Generating BLSTM model: ")
    bltsm_ = BLSTM(dataframe, "trained")
    bltsm_.train()
    
    endtime = time.time()
    
    print("==> Total time: " + str(endtime - starttime))
    
    bltsm_.test()