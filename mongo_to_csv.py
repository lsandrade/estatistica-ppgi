#   -*- coding: utf-8 -*-
# importando pymongo
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import json
import sys
import re
import unicodedata


def remove_special_chars(text):
	#removendo quebra de linhas e pontuação
	text = text.replace('\n',' ').replace('?','').replace('!','').replace('.','').replace(',','').replace(':','')
	#print(text)
	#removendo links/URLs
	text = re.sub(r"http\S+", "", text)
	return text

def remove_stop_words(text):
	s = open("stopwords_pt.txt","r")
	stop_words = s.read().splitlines()
	for stop_word in stop_words:
		text = text.replace(" "+stop_word+" "," ")
		text = text.replace("RT ","")
	return text


# criando cliente (127.0.0.1:27017)
client = MongoClient()

# selecionando banco de dados
db = client.bela

# selecionando collection
coll = db.tweets

# contador de tweets inseridos (somente para visualização)
cont = 0
uerror= 0

# abrir arquivo para escrita
f = open("belarecatada.csv","a", encoding='utf-8')


# find all documents
cursor = coll.find()

for document in cursor:
	try:
		payload = document['payload']#.encode(encoding="utf-8", errors="strict") 
		#print(payload)
		# removendo caracteres especiais e pontuação
		text_without_special_chars = remove_special_chars(payload)
		
		# removendo stop words
		text_without_stop_words = remove_stop_words(text_without_special_chars)

		#print(text_without_stop_words)
		# escrevendo num arquivo externo
		f.write(text_without_stop_words+"\n")
		
		print (str(cont) + " tweets passaram\n")
	except KeyError:
		print ("############Acho que o tweet "+str(cont)+" não tem variável payload ############\n")
	except UnicodeError:
		print("*** "+document['payload'].encode()+" ***")
		uerror+=1
	cont+=1
	
print("Erros de unicode: "+str(uerror))

f.close()    