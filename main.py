import wordnet
import re
import simword
from janome.tokenizer import Tokenizer

# print(simword.get_similar_word(dai))
tokenizer = Tokenizer()

def print_maimai(C = None):
    if C == None:
        C = wordnet.get_rondom_words(1)[0]

    A = wordnet.get_hype_word(C)
    B = simword.get_similar_word(C)
    if len(A) == 0:
        return

    if A[-1] != 'い' and A[-1] != 'う' and A[-1] != 'く' and A[-1] != 'す' and A[-1] != 'つ' and A[-1] != 'ぬ' and A[-1] != 'ぶ' and A[-1] != 'む' and A[-1] != 'る':
        A += 'な'
    
    print("Q.%s%sってな～んだ A.%s" % (A,B, C)) 
    return

def print_gattai():
    A,B = wordnet.get_rondom_words(2, (1,3))
    #print(A + " " + B)
    #         
    C = simword.get_similar_word(A + B)

    if A[-1] != 'い' and A[-1] != 'う' and A[-1] != 'く' and A[-1] != 'す' and A[-1] != 'つ' and A[-1] != 'ぬ' and A[-1] != 'ぶ' and A[-1] != 'む' and A[-1] != 'る':
        A += 'な'
    print("Q.%s%sってな～んだ A.%s" % (A,B, C)) 
    return

def print_shovel(C = None):
    if C == None:
        C = wordnet.get_rondom_words(1)[0]

    simC =simword.get_similar_word(C)
    A = wordnet.get_syndef(simC)
    B = wordnet.get_hype_word(C)
    if len(A) == 0:
        return

    A = re.sub(r"（.+?）", "", A)
    if tokenizer.tokenize(A)[-1].part_of_speech.split(',')[0] == '名詞':
        A += 'の'

    
    print("Q.%s%sってな～んだ A.%s (%s)" % (A,B, C, simC)) 

def print_saibansho(A = None):
    if A == None:
        A = wordnet.get_rondom_words(1)[0]
        
    C = wordnet.get_include_word(A)
    if C == None:
        return
    B = wordnet.get_hype_word(C)
    print("Q.%sの%sってな～んだ A.%s" % (A,B, C)) 


while True:
    print_saibansho("裁判")