import sqlite3
import re
from pykakasi import kakasi
import random

conn = sqlite3.connect("wnjpn.db")

class Word_Tree:
    class node:
        def __init__(self, name, children=None):
            self.name = name  # String
            self.children = children  # List of Class node

        # 結果表示用
        def display(self, indent = 0):
            if self.children != None:
                print(' '*indent + self.name)
                for c in self.children:
                    c.display(indent+1)
            else:
                print(' '*indent + self.name)
    # 下位の語が未登録の場合、再帰的に呼ばれる関数
    def recrusive_register(self, term):
        for term in self.hierarchy_dict[term]:
            if term not in self.node_tree_dict:
                if term in self.hierarchy_dict:
                    self.recrusive_register(term)
                    self.node_tree_dict[term] = self.node(self.synset_name_dict[term], [self.node_tree_dict[t] for t in self.hierarchy_dict[term]])
                else:
                    self.node_tree_dict[term] = self.node(self.synset_name_dict[term])

    
    def __init__(self):
        # 上位-下位の関係にある概念の抽出
        self.hierarchy_dict = {}  # key:上位語(String), value:下位語(List of String)
        self.n_term_set = set()  # 下位語に含まれる単語集合

        cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")  # 上位語-下位語の関係にあるものを抽出
        for row in cur:
            b_term = row[0]
            n_term = row[1]

            if b_term not in self.hierarchy_dict:
                self.hierarchy_dict[b_term] = []

            self.hierarchy_dict[b_term].append(n_term) 
            self.n_term_set.add(n_term)
            

        self.top_concepts = list(set(self.hierarchy_dict.keys()) - self.n_term_set)

        print("上位語に含まれる単語の中で下位語に含まれない単語の数 ： %s" % len(self.top_concepts))

        # synset(概念)のIDから、概念の名称に変換する辞書の作成
        self.synset_name_dict = {}  # key:synsetのID, value:synsetの名称
        cur = conn.execute("select synset,name from synset")
        for row in cur:
            self.synset_name_dict[row[0]] = row[1]
        for k,v in self.synset_name_dict.items():
            print("%s : %s" % (k,v))
            break

        # データ投入
        self.node_tree_dict = {}
        for k in self.top_concepts:  # 最上位の語を起点として木構造を作成
            self.recrusive_register(k)
            self.node_tree_dict[k] = self.node(self.synset_name_dict[k], [self.node_tree_dict[term] for term in self.hierarchy_dict[k]])

    
wordid_dict = {}
word_dict = {}
kana_dict = {}

kakasi = kakasi()
kakasi.setMode('K', 'H')
kakasi.setMode('J', 'H')
converter = kakasi.getConverter()
    
cur = conn.execute("select lemma,wordid from word where lang='jpn'")
for row in cur:
    kana = converter.do(row[0])
    if kana in kana_dict or row[0] in word_dict:
        continue
    wordid_dict[row[1]] = row[0]
    word_dict[row[0]] = row[1]
    kana_dict[kana] = row[1]

def get_synset(wordid):
    return list(conn.execute("select synset from sense where wordid='%s'" % wordid))

def get_root(synset):
    return
    
def is_kanji(word):
    if converter.do(word) == word:
        return False
    return True

def get_include_word(word, wari = 0):
    cand = []
    kanword = word
    word = converter.do(word)
    for fr in range(len(word)):
        for to in range(fr + 2, len(word) + 1):
            if (fr == 0 and to == len(word)) or (1.0* (to-fr)/len(word)) < wari:
                continue
            kana = converter.do(word[fr:to])
            if kana in kana_dict:
                wordid = kana_dict[kana]
                kanji = wordid_dict[wordid]
                if is_kanji(kanji) and kanji in kanword:
                    continue
                cand.append(wordid)

    if len(cand) == 0:
        return None

    return wordid_dict[random.choice(cand)]

def get_many_meaning_word():

    # word_tree.node_tree_dict[word_tree.top_concepts[10]].display()

    return

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

def get_syndef(word):
    wordid = get_wordid(word)
    synsets = list(conn.execute("select synset from sense where wordid='%s'" % wordid))
    defs = list(conn.execute("select def from synset_def where (lang='jpn' and synset='%s')" % random.choice(synsets)[0]))
    return random.choice(defs)[0]

def get_hype_word(word, count = 1):
    wordid = get_wordid(word)

    path = get_longest_path(wordid)

    cand = []

    for pathpos in range(int(len(path) / 3), int(len(path) / 2) + 1):
        synset = path[pathpos]

        curid = list(conn.execute("select wordid from sense where synset='%s'" % synset))
        for idd in curid:
            ret = str(list(conn.execute("select lemma,pos from word where (wordid='%s')" % idd))[0][0])
            if ret == word:
                continue
            if re.search('[a-z]',ret) == None:
                cand.append(ret)

    if len(cand) > 0:
        return random.sample(cand, 2) if count > 1 else random.choice(cand)
    else:
        return ""

def get_rondom_words(num, lemma_len = (0,99999)):
    ret = []

    while len(ret) == 0:
        words = list(conn.execute("select lemma from word where (pos='n' and lang='jpn' and lemma_len > ? and lemma_len < ?) order by random() limit ?", (lemma_len[0], lemma_len[1], str(num))))

        for word in words:
            if re.search('[A-zＡ-Ｚａ-ｚ１-９０]',word[0]) != None:
                continue
            ret.append(word[0])
    
    return ret