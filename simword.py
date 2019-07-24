import requests
import re
import wordnet
import numpy as np
from pykakasi import kakasi

def conv_to_kana(word):
    responce = requests.post('https://labs.goo.ne.jp/api/hiragana', 
        data = {"app_id":"c6d687dfedd172e4a2b30cc086513cfbb23f8c039c8c157fe08760b3df4092fa","request_id":"test","sentence":word,"output_type":"hiragana"})

    return responce.json["converted"]


kakasi = kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')
converter = kakasi.getConverter()
boin = ['a','i','u','e','o']

def get_distance(wordx, wordy):
    wordx = converter.do(wordx)
    wordy = converter.do(wordy)

    #print(wordx + " " + wordy)
    dp = np.empty((len(wordx) + 1, len(wordy) + 1))
    
    for i in range(len(wordx) + 1):
        dp[i][0] = i
    for i in range(len(wordy) + 1):
        dp[0][i] = i
    
    for i in range(1, len(wordx) + 1):
        for j in range(1, len(wordy) + 1):
            dp[i][j] = min(
                dp[i-1][j] + 1 + int(wordx[i-1] in boin),
                dp[i][j-1] + 1 + int(wordy[j-1] in boin),
                dp[i-1][j-1] + int(wordx[i-1] != wordy[j-1])) + int(wordx[i-1] in boin or wordy[j-1] in boin)

    return dp[len(wordx)][len(wordy)]


def get_similar_word(word):

    words = wordnet.get_rondom_words(4000)
    bestscore = 999999
    bestword = ''

    for cur_word in words:
        if re.search('[A-z,Ａ-Ｚ,ａ-ｚ]',cur_word) != None:
            continue
        if word == cur_word:
            continue
        score = get_distance(word,cur_word)
        #print("%s %s" % (score, cur_word))
        if score < bestscore:
            bestscore = score
            bestword = cur_word

    return bestword