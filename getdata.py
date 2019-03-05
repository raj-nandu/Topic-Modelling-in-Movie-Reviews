from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle

reviews = []
wiki = "https://wogma.com/movies/basic/"
page = urlopen(wiki)
soup = BeautifulSoup(page,'lxml')
linkw = "https://wogma.com/"
all_links = soup.find_all("a")

print("Total Number of reviews = " + str(len(all_links)))
count = 0
for link in all_links:
    if count % 10 == 0:
        with open("reviews.pkl", 'wb') as data:
            pickle.dump(reviews, data)
    if link.string == 'wogma review':
        review_link = linkw + link.get("href")
        review = urlopen(review_link)
        review_soup = BeautifulSoup(review, 'lxml')
        output = ""
        r = review_soup.find('div', class_='wogma-review')

        paras = r.find_all('p')
        for p in paras:
            output += p.text
        print(output)

        reviews.append(output)
        count += 1

with open("reviews.pkl", 'wb') as data:
    pickle.dump(reviews, data)
print(str(reviews))
