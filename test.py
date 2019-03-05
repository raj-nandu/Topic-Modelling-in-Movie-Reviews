# importing all the dependencies
import gensim
from gensim import corpora
from nltk.corpus import stopwords
import string
import pickle
from nltk.stem.wordnet import WordNetLemmatizer


#cleaning the dataset
with open("dumped_data.pkl", 'rb') as d:
    data = pickle.load(d)
reviews = data[-1]
print(str(len(reviews)))

stopwords_set = set(stopwords.words('english'))
print(stopwords_set)
punctuations = set(string.punctuation)
print(punctuations)
lemmatizer = WordNetLemmatizer()

def clean_review(review):
    # Removing stopwords
    s = " ".join([word for word in review.lower().split() if word not in stopwords_set])
    # Removing punctuations
    p = ''.join(letter for letter in s if letter not in punctuations)
    # Lemmatizing words eg. loves -> love
    out = " ".join(lemmatizer.lemmatize(word) for word in p.split())
    return out


cleaned_reviews = [clean_review(review).split() for review in reviews]


# length of cleaned reviews
len(cleaned_reviews)


# Creating a dictionary
dictionary = corpora.Dictionary(cleaned_reviews)


inp = [dictionary.doc2bow(review) for review in cleaned_reviews]


# Creating lda model
lda = gensim.models.ldamodel.LdaModel
ldamodel = lda(inp, num_topics=50, id2word=dictionary, passes=100)
a = ldamodel.print_topics(num_topics=15, num_words=50)

print(a)

# inference
# Copy the input review in the test variable

test = "So, Airlift has one of Akshay Kumar's best performances - along with other sterling acts. Rich Indian-origin businessman Ranjit Katyal (Akshay) loves profits and dislikes the idea of India. But Ranjit's golden life in the desert crumbles when Iraqi forces invade Kuwait. Suddenly, people are savagely shot in the streets, houses looted, buildings blown up, tanks taking over, choppers hovering maliciously amidst minarets. Airlift features Akshay at his best - based on real-life characters, there's little khiladi-wala swag in Akshay's performance and more mature control. As Ranjit, who goes from protecting his kin to his countrymen, Akshay does a polished, restrained, powerful job. Nimrat conveys brittle edginess - she asks Ranjit, Ye Indian-Indian khelna, kya drama ho raha hai? - but grows into a woman who loves her husband's humanitarian heart. Certain cameos are outstanding. Prakash Belawadi brings alive surly, suspicious George, Kumud Mishra deeply impresses as a quietly determined MEA babu and Inaamulhuq oozes smooth menace as he quotes 'Amytabh Bachchan' to Ranjit - before showing him his business partner, hanging from a crane outside a palace full of bloodied marble and broken glass. Airlift's scale is impressive and editing (Hemanti Sarkar) deft. Some sequences - Iraqi soldiers brutally molesting an Indian girl, looting even onions, cheerily singing 'Ek Do Teen', dragging out a young mother, so the boys can have some fun with her - are intense. But the movie could've increased this intensity, the horror and taut, time-ticking dread that typify unforgettable siege/rescue films like Hotel Rwanda (2004), where you vividly felt humanity running out each second. Airlift depicts desperation but with more sound and light than darkness, more broad strokes than fine detail. Yet, Airlift works because it conveys a time when armies will attack civilians - you're struck by how IS was born from the Iraqi army's core - and raises Bollywood's generic bar. Plus, it movingly celebrates the most beautiful flag in the world."
test = reviews[50]
test = clean_review(test).split()
print(test)

test = dictionary.doc2bow(test)
print(ldamodel[test])
a = list(sorted(ldamodel[test], key=lambda x: x[1]))

print(a)

# Least related topic to the test review is the first element of the sorted list a
print("The words associated with least related topic to the test review are")
print(ldamodel.print_topic(a[0][0]))

# Most probable topic related to the test review is the last element of the sorted list a
print("The words associated with most probable topic related to the test review are")
print(ldamodel.print_topic(a[-1][0]))

#loading topics and inference
topic_dict = {}
topics = open('topics.txt',"r")
for line in topics:
    a, b = line.split()
    topic_dict[int(a)] = b
topics.close()
print(topic_dict)
test = "So, Airlift has one of Akshay Kumar's best performances - along with other sterling acts. Rich Indian-origin businessman Ranjit Katyal (Akshay) loves profits and dislikes the idea of India. But Ranjit's golden life in the desert crumbles when Iraqi forces invade Kuwait. Suddenly, people are savagely shot in the streets, houses looted, buildings blown up, tanks taking over, choppers hovering maliciously amidst minarets. Airlift features Akshay at his best - based on real-life characters, there's little khiladi-wala swag in Akshay's performance and more mature control. As Ranjit, who goes from protecting his kin to his countrymen, Akshay does a polished, restrained, powerful job. Nimrat conveys brittle edginess - she asks Ranjit, Ye Indian-Indian khelna, kya drama ho raha hai? - but grows into a woman who loves her husband's humanitarian heart. Certain cameos are outstanding. Prakash Belawadi brings alive surly, suspicious George, Kumud Mishra deeply impresses as a quietly determined MEA babu and Inaamulhuq oozes smooth menace as he quotes 'Amytabh Bachchan' to Ranjit - before showing him his business partner, hanging from a crane outside a palace full of bloodied marble and broken glass. Airlift's scale is impressive and editing (Hemanti Sarkar) deft. Some sequences - Iraqi soldiers brutally molesting an Indian girl, looting even onions, cheerily singing 'Ek Do Teen', dragging out a young mother, so the boys can have some fun with her - are intense. But the movie could've increased this intensity, the horror and taut, time-ticking dread that typify unforgettable siege/rescue films like Hotel Rwanda (2004), where you vividly felt humanity running out each second. Airlift depicts desperation but with more sound and light than darkness, more broad strokes than fine detail. Yet, Airlift works because it conveys a time when armies will attack civilians - you're struck by how IS was born from the Iraqi army's core - and raises Bollywood's generic bar. Plus, it movingly celebrates the most beautiful flag in the world."
test = clean_review(test).split()
#print(test)

test = dictionary.doc2bow(test)
a = list(sorted(ldamodel[test], key=lambda x: x[1]))
# Least related topic to the test review is the first element of the sorted list a
print("The words associated with least related topic to the test review are")
print(ldamodel.print_topic(a[0][0]))
if a[0][0] in topic_dict:
    print(topic_dict[a[0][0]])
else:
    print("Unknown topic")

# Most probable topic related to the test review is the last element of the sorted list a
print("The words associated with most probable topic related to the test review are")
print(ldamodel.print_topic(a[-1][0]))
if a[-1][0] in topic_dict:
    print(topic_dict[a[-1][0]])
else:
    print("Unknown topic")
 

    
    
    
    
# Visualization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


fiz=plt.figure(figsize=(15,30))
for i in range(15):
    df=pd.DataFrame(ldamodel.show_topic(i), columns=['term','prob']).set_index('term')
#     df=df.sort_values('prob')
    
    plt.subplot(5,3,i+1)
    plt.title('topic '+str(i+1))
    sns.barplot(x='prob', y=df.index, data=df, label='Cities', palette='Reds_d')
    plt.xlabel('probability')
    

plt.show()
