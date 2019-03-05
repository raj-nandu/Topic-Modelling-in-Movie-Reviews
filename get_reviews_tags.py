from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle


wiki = "https://wogma.com/movies/basic/"
page = urlopen(wiki)
soup = BeautifulSoup(page,'lxml')
linkw = "https://wogma.com/"
all_links = soup.find_all("a")

print("Total Number of reviews = " + str(len(all_links)))
count = 1
movie_names = []
movie_tags = []
reviews = []
reviews_with_tags = []
for link in all_links:
    if count % 10 == 0:
        with open("dumped_data.pkl", 'wb') as data:
            dumped_data = (movie_names, reviews, movie_tags, reviews_with_tags)
            pickle.dump(dumped_data, data)
    
        # if count >=100:
        #     break
    if link.string == 'wogma review':
        try:
            review_link = linkw + link.get("href")
            review = urlopen(review_link)
            review_soup = BeautifulSoup(review, 'lxml')
            output = ""
            r = review_soup.find('div', class_='wogma-review')
    
            paras = r.find_all('p')
            for p in paras:
                output += p.text
            # print(output)
    
            # tagging reviews
            t = []
            r = review_soup.find('div', {"id": 'parental_guidance'})
            # print(r.text)
            if r is not None:
                tags = r.find_all('li')
                print(str(tags))
                # violence
                
                if 'None' not in tags[0].text.split():
                    t.append('violence')
                else:
                    t.append('non_violent')
                # clean
                if 'Clean' not in tags[1].text.split():
                    t.append('clean_language')
                else:
                    t.append("swear_words")
                if 'None' not in tags[2].text.split():
                    t.append('sexual_content')
                else:
                    t.append('no_sexual_content')

            # print(t)
    
            # genre
            div_genre = review_soup.find_all('div', class_='coloring')
            temp = div_genre[-1].text
            temp = temp.replace(',', '').lower()
            temp = temp.strip('Genres:')
            temp = temp.split()
            temp = temp[1:]
            # print(temp)
            movie_tags.append(t+temp)
            reviews.append(output)
            movie_name = review_soup.find('h3', class_='title').text.lower()
            print(movie_name)
            movie_names.append(movie_name)
            for i in t+temp:
                output += " " + i
            reviews_with_tags.append(output)
            print("Movie Number = " + str(count))
            count += 1
        except:
            print("Exception Occured")


dumped_data = (movie_names, reviews, movie_tags, reviews_with_tags)
with open("dumped_data.pkl", 'wb') as data:
    pickle.dump(dumped_data, data)
print(str(movie_names))
print(str(reviews))
print(str(movie_tags))
print(str(reviews_with_tags))
