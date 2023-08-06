def convert():
    with open('input.txt', 'r') as f:
        content = f.read()
        # lines = f.readlines()
        #print("Original: \n" + content+"\n")
        #print("Converted to binary: ")
        res = ''.join(format(i, '08b') for i in bytearray(content, encoding ='utf-8'))
        #print(str(res)+ "\n")
    return res
