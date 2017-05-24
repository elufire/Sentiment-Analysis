

from __future__ import division
import matplotlib.pyplot as spplot
import re
import collections

#the following code reads in and stores the data on the lexicon values
data=open("sent_lexicon.csv", "r")
data=data.read()
data=data.split("\n")

for i in range(0, len(data)):
    if len(data[i]) == 0:
        del(data[i])
        continue
    
for index in range(0, len(data)):
    data[index]=data[index].split(",")
    data[index][1]=float(data[index][1])
    
word, score = zip(*data)

lex_data = dict(zip(word, score))

#print(lex_data)

#the following allows the user to input the speech name they want to be analyzed
speech = open(raw_input("Please enter Speech Name: "), 'r')
speech = speech.read()
#speech = speech.split("\n")

#the following reads in and stores and splits the speeches into individual words
for i in range(0, len(speech)):
    if len(speech[i]) == 0:
        del(speech[i])
        continue
    
speech_words=re.split(r' -- |[ ?!,.:$\";]+', speech)
speech_words=list(speech_words)

for i in range(0, len(speech_words)):
    speech_words[i]=speech_words[i].lower()

speech_words= [i for i in speech_words if not (i.isdigit() or i[0].isdigit())]

for i in range(0, len(speech_words)):
    if speech_words[i] == '\n':
        del(speech_words[i])
        break
 
speech_words=sorted(speech_words)    
speech_words_unique=set(speech_words)
speech_words_unique=sorted(speech_words_unique)

speech_words_count=collections.Counter(speech_words)

#the following code counts all the words that have lexicon values and counts them into the correct category
count_weakneg = 0
count_neg = 0
count_neutral = 0
count_weakpos = 0
count_pos = 0
count_total = 0

for word in speech_words_unique:
    
    if lex_data.has_key(word):
        if lex_data.get(word)<-0.6:
            count_neg += speech_words_count.get(word)
        elif lex_data.get(word)<-0.2:
            count_weakneg += speech_words_count.get(word)
        elif lex_data.get(word)<=0.2:
            count_neutral += speech_words_count.get(word)
        elif lex_data.get(word)<=0.6:
            count_weakpos += speech_words_count.get(word)
        elif lex_data.get(word)>0.6:
            count_pos += speech_words_count.get(word)

#following calculates the percentage for each category
count_total =  count_neg + count_weakneg + count_neutral + count_weakpos + count_pos
all_count=[count_neg, count_weakneg, count_neutral, count_weakpos, count_pos]
count_num=[0,1,2,3,4]
all_percentages=[count_neg/count_total, count_weakneg/count_total, count_neutral/count_total, count_weakpos/count_total, count_pos/count_total]
count_names = ["Negative", "Weak Negative", "Neutral", "Weak Positive", "Positive"]
#print(all_percentages, all_count, count_total)
#print(all_count)
#print(speech_words_count, count_neg, count_weakneg, count_neutral, count_weakpos, count_pos)    

#the following is the code that handles the actual graphing
spplot.xlabel("Sentiment")
spplot.ylabel("Percent of Words")

tick_pos=[0, 1, 2, 3, 4]
spplot.xticks(tick_pos, count_names)
spplot.bar(count_num, all_percentages)
#spplot.set_xlim([0,len(1)])
spplot.show()
#spplot.bar(range(1,5), all_percentages)

