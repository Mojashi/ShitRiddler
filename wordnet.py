import sqlite3
import re
import random

conn = sqlite3.connect("wnjpn.db")

def get_wordid(word):
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    
    word_id = -1  #temp 
    for row in cur:
        word_id = row[0]

    return word_id

def get_longest_path(wordid):

    cur_path = []
    synsets = conn.execute("select synset from sense where wordid='%s'" % wordid)

    for synsetid in synsets:
        buf_path = [synsetid]
        cur_synset = synsetid

        while True:
            par = list(conn.execute("select synset1 from synlink where (link='hypo' and synset2='%s')" % cur_synset))
            if len(par) == 0:
                break
            cur_synset = par[0][0]
            buf_path.append(cur_synset)
        
        if len(cur_path) < len(buf_path):
            cur_path = buf_path

    return cur_path

def get_hype_word(word):
    wordid = get_wordid(word)

    path = get_longest_path(wordid)

    synset = path[int(len(path) / 3)]


    cand = []
    curid = list(conn.execute("select wordid from sense where synset='%s'" % synset))
    for idd in curid:
        ret = str(list(conn.execute("select lemma,pos from word where (wordid='%s')" % idd))[0][0])
        if ret == word:
            continue
        if re.search('[a-z]',ret) == None:
            cand.append(ret)

    if len(cand) > 0:
        return random.choice(cand)
    else:
        return ""

def get_rondom_words(num, lemma_len = (0,99999)):
    words = list(conn.execute("select lemma from word where (pos='n' and lang='jpn' and lemma_len > ? and lemma_len < ?) order by random() limit ?", (lemma_len[0], lemma_len[1], str(num))))
    ret = []
    for word in words:
        ret.append(word[0])

    return ret