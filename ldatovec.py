import gensim
from gensim import corpora
from nltk.corpus import stopwords
import string
import pickle
from nltk.stem.wordnet import WordNetLemmatizer

#cleaning the dataset
with open("reviews.pkl", 'rb') as data:
    reviews = pickle.load(data)
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
print(str(len(cleaned_reviews[0])))

# creating a dictionary
dictionary = corpora.Dictionary(cleaned_reviews)

inp = [dictionary.doc2bow(review) for review in cleaned_reviews]
# print(str(len(inp[0])))
# print(len(dictionary))

lda = gensim.models.ldamodel.LdaModel
ldamodel = lda(inp, num_topics=5, id2word=dictionary, passes=20)
a = ldamodel.print_topics(num_topics=5, num_words=5)
print(a)


# --------------------inference--------------------------------

test = "This is one of the best movie i have ever watched. I will give it 5 stars"
test = clean_review(test).split()
test = dictionary.doc2bow(test)
print(ldamodel[test])
a = list(sorted(ldamodel[test], key=lambda x: x[1]))

ldamodel.print_topic(a[0][0])

ldamodel.print_topic(a[-1][0])