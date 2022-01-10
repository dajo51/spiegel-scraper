#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request
import time as t
import json
import csv


# In[5]:


issues_links = []
article_list = []

# set range to scrape 
for year in range(2000, 2022):
    for issue in range(1, 54):
        with urllib.request.urlopen(f"https://www.spiegel.de/spiegel/print/index-{year}-{issue}.html") as response:
           html = response.read()

        # get all article links, titles, year & issue numbers for set range 
        soup = BeautifulSoup(html, 'html.parser')
        for a in soup.findAll("article"):
            link = a.find("a")
            article_list.append([link["href"], link["title"], year, issue])


        # print out information as checkpoint 
        print("Issue", issue, year, "added! Time needed to scrape articles:", round((5*len(article_list)/60), 2), "minutes")
        print("Total articles:", len(article_list))
        #t.sleep(1)


# In[2]:


# read article list from file
article_list = []
with open('article_links_complete.csv', newline='') as csvfile:
    article_list = list(csv.reader(csvfile))
    
print(len(article_list))


# In[ ]:


# save article links to csv
print(len(article_list))

with open("article_links_test.csv", "w", encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(article_list)


# In[3]:


data = {}
article_id = 1
temp = 2017
for i in article_list[88977:]:
    article_id = int(article_list.index(i)) + 1
    if int(i[2]) > temp:
        # save data into utf-8 json
        with open(f"data_{temp}.json", "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        data = {}
        print(f"Finished adding {temp}.")
        temp += 1
    
    # scrape get article data from link list
    with urllib.request.urlopen(i[0]) as response:
       article = response.read()
    article_soup = BeautifulSoup(article, 'html.parser')
    ps = article_soup.findAll("p", class_=False)
    text = ""
    
    #structurize data into human readable dict
    for p in ps:
        text += p.text
    article_data = {  
        "link": i[0],
        "date": article_soup.find("meta", {"name" : "date"})["content"],
        "year": i[2],
        "issue": i[3],
        "keywords": article_soup.find("meta", {"name" : "news_keywords"})["content"],
        "author": article_soup.find("meta", {"name" : "author"})["content"],
        "title": i[1],
        "description": article_soup.find("meta", {"name" : "description"})["content"],
        "text": text
    }
    data[article_id] = article_data
    print("Artikel", article_id, "hinzugefügt")
    #t.sleep(1)


# In[4]:


# save data into utf-8 json
with open('data_test_rest.json', 'w', encoding='utf8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

