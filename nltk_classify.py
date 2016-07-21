## coding: utf-8

## importar biblioteca NLTK com funções de Machine Learning
import nltk
import cloudpickle
## importando tweets positivos
pos = open('positives.txt','r')
lines = pos.read().splitlines()
pos_tweets = []
for tweet in lines:
	pos_tweets.append((tweet,'positive'))
#print pos_tweets
pos.close()


## importando tweets negativos
neg = open('negatives.txt','r')
lines = neg.read().splitlines()
neg_tweets = []
for tweet in lines:
	neg_tweets.append((tweet,'negative'))
#print neg_tweets
neg.close()

## importando tweets neutros
neu = open('neutrals.txt','r')
lines = neu.read().splitlines()
neu_tweets = []
for tweet in lines:
	neu_tweets.append((tweet,'neutral'))
#print neu_tweets
neu.close()

## criando vetor de palavras/sentimento
tweets = []
for (words, sentiment) in pos_tweets + neg_tweets + neu_tweets:
	words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
	tweets.append((words_filtered, sentiment))
#print tweets

## Dados de teste
test_tweets = []
test = open('test.txt','r')
lines = test.read().splitlines()
for tweet in lines:
	tweet = tweet.split(',')
	words = tweet[0].split(' ')
	test_tweets.append((words,tweet[1]))
#print test_tweets
test.close()


## classifier
def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	wordlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

word_features = get_word_features(get_words_in_tweets(tweets))
## print word_features

## extrair features
def extract_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

## TRAINNING
training_set = nltk.classify.apply_features(extract_features, tweets)
#print (training_set)

classifier = nltk.NaiveBayesClassifier.train(training_set)

print ('accuracy:', nltk.classify.util.accuracy(classifier, training_set))
classifier.show_most_informative_features()

#print (cloudpickle.dumps(classifier))

#print classifier.show_most_informative_features(32)

## CLASSIFY

f = open('belarecatada.csv','r',encoding='utf-8',errors='replace')
r = open("result.txt","a")
rows = f.read().splitlines()

count = 0
pos = 0
neg = 0
neu = 0
for tweet in rows:
	#tweet = 'bela recatada do lar causando'
	count += 1
	result = classifier.classify(extract_features(tweet.split()))
	r.write(result+"\n");
	if result == 'positive':
		pos += 1
	elif result == 'negative':
		neg += 1
	elif result == 'neutral':
		neu +=1
	print (str(count)+" tweets classificados. Positivos: "+str(pos)+". Negativos: "+str(neg)+". Neutros: "+str(neu)+".\n")
	#print extract_features(tweet.split())

f.close()
r.close()
