import heapq
import json
from bitarray import bitarray

with open('huffman_file.txt','r', encoding="utf-8") as file:
    dane = file.read()
    


class Node:
    def __init__(self,value,name):
        self.name = name
        self.value = value
        self.child_left = None
        self.child_right = None
        

    def add_child_left(self,child):
        self.child_left = child
        
    
    def add_child_right(self,child):
        self.child_right = child
        
        
    def delete_child_left(self):
        self.child_left = None
        
        
    def delete_child_right(self):
        self.child_right = None
        
        
        
    def __repr__(self):
        #return f"{self.value}, left child: {self.child_left}, right child: {self.child_right}"
        return f"{self.value,self.name}"
       
def concordance(doc):
    if type(doc) != str:
        return "not text"
    con = dict()
    for letter in doc:
        if letter not in con:
            con[letter] = 1
        else: 
            con[letter] += 1
            
    return con

con = concordance(dane)
#print(con)
result = ''
codes = {}
nodes = dict()


def mark(node, current_code=""):
    global codes
    global nodes
    if node.child_left:
        codes[node.child_left.name] = current_code + '0'
        mark(nodes[node.child_left.name], current_code + '0')
        
        
    if node.child_right:
        codes[node.child_right.name] = current_code + '1'
        mark(nodes[node.child_right.name], current_code + '1')
    

def huffman(con):
    global nodes
    global codes
    queue = []
    for i in con.keys():
        queue.append([con[i],i])
    heapq.heapify(queue)
    
    while len(queue) > 1:
        
        a = heapq.heappop(queue)
        b = heapq.heappop(queue)
        a_node = Node(a[0],a[1])
        b_node = Node(b[0],b[1])
        new_val = a[0] + b[0]
        new_name = a[1] + b[1]
        new_node = Node(new_val, new_name)
        new_node.add_child_right(a_node)
        new_node.add_child_left(b_node)
        if a_node.name not in nodes.keys():
            nodes.update({
                a_node.name: a_node
            })
        if b_node.name not in nodes.keys():
            nodes.update({
                b_node.name: b_node
            })
        if new_node.name not in nodes.keys():
            nodes.update({
                new_node.name: new_node
            })
        heapq.heappush(queue, [new_val, new_name])
        root = new_node
        
    for i in nodes.keys():
        codes.update({
            i: ''
        })
    mark(root)
    
    return nodes



huffman(con)

for d in dane:
    result += codes[d]
#print(result)

b = bitarray(result)                

with open('results.bin', 'wb') as f:
    header = json.dumps(codes).encode('utf-8')
    f.write(len(header).to_bytes(4, 'big'))  
    f.write(header)
    f.write(len(result).to_bytes(4, 'big'))  
    b.tofile(f)          
