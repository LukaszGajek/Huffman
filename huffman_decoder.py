from bitarray import bitarray
import json

b = bitarray()
with open('results.bin','rb') as res:
    header_len = int.from_bytes(res.read(4), "big")
    header = res.read(header_len)
    codes = json.loads(header.decode("utf-8"))
    
    bit_len = int.from_bytes(res.read(4), "big")
    
    b.fromfile(res)


    
reverse_codes = dict()
for key in codes.keys():
    if len(key) == 1:
        reverse_codes.update({
            codes[key]: key
        }) 
    
#print(reverse_codes)
    
data = b.to01()
#print(data)
result = ''
current = ''
for i in range(bit_len):
    current += data[i]
    if current in reverse_codes.keys():
        result += reverse_codes[current]
        current = ''

#print(result)

with open('decoded.txt', 'w') as f:
    f.write(result)        


