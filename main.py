import wordnet
import re
import simword

# print(simword.get_similar_word(dai))

def print_maimai():
    C = wordnet.get_rondom_words(1)[0]
    if re.search('[A-z,Ａ-Ｚ,ａ-ｚ]',C) != None:
        return
    A = wordnet.get_hype_word(C)
    B = simword.get_similar_word(C)
    if len(A) == 0:
        return

    if A[-1] != 'い' and A[-1] != 'う' and A[-1] != 'く' and A[-1] != 'す' and A[-1] != 'つ' and A[-1] != 'ぬ' and A[-1] != 'ぶ' and A[-1] != 'む' and A[-1] != 'る':
        A += 'な'
    
    print("Q.%s%sってな～んだ A.%s" % (A,B, C)) 
    return

def print_gattai():
    A,B = wordnet.get_rondom_words(2, (1,4))
    #print(A + " " + B)

    if re.search('[A-z,Ａ-Ｚ,ａ-ｚ]',A) != None:
        return
    if re.search('[A-z,Ａ-Ｚ,ａ-ｚ]',B) != None:
        return
        
    C = simword.get_similar_word(A + B)

    if A[-1] != 'い' and A[-1] != 'う' and A[-1] != 'く' and A[-1] != 'す' and A[-1] != 'つ' and A[-1] != 'ぬ' and A[-1] != 'ぶ' and A[-1] != 'む' and A[-1] != 'る':
        A += 'な'
    print("Q.%s%sってな～んだ A.%s" % (A,B, C)) 
    return


while True:
    print_gattai()