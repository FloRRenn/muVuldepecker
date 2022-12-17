#########################################
###### Step 3 trong Training Phase ######
#########################################

import re
from keywords_data.default_keywords import *

function_regex = re.compile('FUNC(\d)+')

# Task: 
#   Input : Mảng string chứa gadget_code code, mỗi phần tử là 1 dòng của gadget_code code
#   Output : Mảng string chứa code gagdet đã modify lại tên gọi của biến và hàm
# Ex: 
#   Input : [
#               'int main(int argc, char **argv) {',
#               'while ((c = getopt(argc, argv, "k:s:m:o:h")) != -1) {',
#               'switch (c) {', 
#               'case 1:', 
#               'char text[] = "hello";',
#               'default:', 
#               'char text[] = "bye"; }'
#           ]
#
#   Output :  [   
#               'int main(int argc, char **argv) {',
#               'while ((VAR1 = FUNC1(argc, argv, "k:s:m:o:h")) != -1) {',
#               'switch (VAR1) {', 
#               'case 1:',
#               'char VAR2[] = "";',
#               'default:',
#               'char VAR2[] = ""; }'
#           ]
def modify_gadget(gadget_code):
    # Lưu tên fucntion cùng với tên được modify của nó 
    func_symbols = {}
    # Ex: func_symbols = {
    #   "function_name_1" : "FUNC1",
    #   "function_name_2" : "FUNC2",
    # }
    
    # Lưu tên biến cùng với tên được modify của nó 
    var_symbols = {}
    # Ex: func_symbols = {
    #   "var_name_1" : "VAR1",
    #   "var_name_2" : "VAR2",
    # }

    # Đánh số thứ tự cho function và biến
    func_count = 1
    var_count = 1

    # regex lấy comment
    regex_comment = re.compile('\*/\s*$')
    
    # regex lấy tên function
    regex_fun = re.compile(r'\b([_A-Za-z]\w*)\b(?=\s*\()')
    
    # regex tên biến
    regex_var = re.compile(r'\b([_A-Za-z]\w*)\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()')

    # result
    output = []

    for line in gadget_code:
        # Nếu dòng đó không phải là comment
        if regex_comment.search(line) is None:
            # Chuỗi lưu trong biến hoặc mảng
            # EX:
            #   char a[] = "hello"; => char a[] = "";
            #   char b[3] = ['a', 'b', '$']; => char b[3] = ['', '', ''];
            nostrlit_line = re.sub(r'".*?"', '""', line)
            nocharlit_line = re.sub(r"'.*?'", "''", nostrlit_line)
            ascii_line = re.sub(r'[^\x00-\x7f]', r'', nocharlit_line)
   
            # Lấy tên biến, tên function
            func_names = regex_fun.findall(ascii_line)
            var_names = regex_var.findall(ascii_line)

            # Đổi tên function
            for name in func_names:
                # Nếu function name != 'main' != list_keywords 
                if len({name}.difference(main_set)) != 0 and len({name}.difference(keywords)) != 0:
                    # Nếu tên chưa có trong danh sách
                    if name not in func_symbols.keys():
                        func_symbols[name] = 'FUNC' + str(func_count)
                        func_count += 1
                    
                    # Đổi tên
                    ascii_line = re.sub(r'\b(' + name + r')\b(?=\s*\()', func_symbols[name], ascii_line)

            # Tương tự với function
            for name in var_names:
                if len({name}.difference(keywords)) != 0 and len({name}.difference(main_args)) != 0:
                    if name not in var_symbols.keys():
                        var_symbols[name] = 'VAR' + str(var_count)
                        var_count += 1
                        
                    ascii_line = re.sub(r'\b(' + name + r')\b(?:(?=\s*\w+\()|(?!\s*\w+))(?!\s*\()',
                                        var_symbols[name], 
                                        ascii_line)

            output.append(ascii_line)
            
    return output


# Task: 
#   Input : File lưu danh sách gadget code, 
#           mỗi gadget code trong file ngăn cách với nhau bằng "---------------------------------"
#
#   Output : List of Dictionaries
#       ouptut = [
#           {
#               "id" : 0,
#               "gadget_code" : [modified_gadget_code],
#               "exit_code" : 0 or 1
#           },
#           {
#               "id" : 1,
#               "gadget_code" : [modified_gadget_code],
#               "exit_code" : 0 or 1
#           },
#       ]
def extract_modify_gadget_code(filename) -> list:   
    # Mảng lưu gadget code sau khi đã modify
    gadget_codes_map = []
    
    with open(filename, 'r', encoding = "utf-8") as f:
        raw_gadget_code = []
        exit_code = 0
        
        for line in f.readlines():
            # Xóa /t, /n, /r
            line = line.strip()
            
            if line == "---------------------------------":
                # Modify gadget code
                gadget_code = modify_gadget(raw_gadget_code[1:])
                to_dict = {
                    "gadget_code" : gadget_code,
                    "exit_code" : exit_code
                }
                
                # Store gagdet code in List
                gadget_codes_map.append(to_dict)
                
                # reset, move to next gadget code program
                raw_gadget_code = []
                exit_code = 0
            
            elif line.isdigit():
                # exit code
                exit_code = int(line)
                
            else:
                # Add unmodified gadget code
                raw_gadget_code.append(line)
                
    return gadget_codes_map

if __name__ == '__main__':
    test_gadget = [
                    '231 151712/shm_setup.c inputfunc 11',
                    'int main(int argc, char **argv) {',
                    'int a = 10;',
                    'char text[] = "hellooo000";'
                    'for (int i = 0; i < a; i++) {',
                    'if (int(i) % 10 == 0 && int(i) || a > 10) {',
                    'printf("%d", i); }',
                    'return 0; }'
                    ]

    print(modify_gadget(test_gadget))
