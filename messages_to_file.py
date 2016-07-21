#  -*- coding: utf-8 -*-
import sys
import re


def remove_special_chars(text):
	#removendo quebra de linhas e pontuação
	text = text.replace('\n',' ').replace('?','').replace('!','').replace('.','').replace(',','').replace(':','').replace("(",'').replace(")",'').replace("'",'')
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



# contador de tweets inseridos (somente para visualização)
cont = 0

#abrir arquivo para leitura
g = open("neutros.txt","r")

# abrir arquivo para escrita
f = open("neutrals.txt","a")

cursor = g.read().splitlines()

for document in cursor:
	try:
		document = document.split(',')[0]
		# removendo caracteres especiais e pontuação
		text_without_special_chars = remove_special_chars(document)
		
		# removendo stop words
		text_without_stop_words = remove_stop_words(text_without_special_chars)

		# escrevendo num arquivo externo
		f.write(text_without_stop_words+"\n")
		print (text_without_stop_words)

		print (str(cont) + " tweets passaram\n")
	except KeyError:
		print ("############Acho que o tweet "+str(cont)+" não tem variável payload ############\n")
	
	cont+=1

f.close()    