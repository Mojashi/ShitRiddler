import wordnet
import simword

# print(simword.get_similar_word(dai))
while True:
    C = wordnet.get_rondom_words(1)[0]
    if re.search('[A-z,Ａ-Ｚ,ａ-ｚ]',C) != None:
        continue
    A = wordnet.get_hype_word(C)
    B = simword.get_similar_word(C)
    if len(A) == 0:
        continue

    if A[-1] != 'い' and A[-1] != 'う' and A[-1] != 'く' and A[-1] != 'す' and A[-1] != 'つ' and A[-1] != 'ぬ' and A[-1] != 'ぶ' and A[-1] != 'む' and A[-1] != 'る':
        A += 'な'
    

    print("Q.%s%sってな～んだ A.%s" % (A,B, C)) 
