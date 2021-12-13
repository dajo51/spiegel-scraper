from bs4 import BeautifulSoup
import urllib.request
import time as t
import json
import csv


issues_links = []
article_list = []

for year in range(2000, 2022):
    for issue in range(1, 52):
        issues_links.append(f"https://www.spiegel.de/spiegel/print/index-{year}-{issue}.html")
        
for issue in issues_links:
    with urllib.request.urlopen(issue) as response:
       html = response.read()
    
    # get all article links and titles, then choose amount of articles to scrape
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.findAll("article"):
        link = a.find("a")
        article_list.append([link["href"], link["title"]])
        
    # article_list = article_list[:100]

    print("Issue added! Time needed to scrape articles:", round((5*len(article_list)/60), 2), "minutes")
    print("Total articles:", len(article_list))
    t.sleep(5)

# save article links to csv
print(len(article_list))

with open("article_links.csv", "w", encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(article_list)

#article_list = article_list[:100]
data = {}
article_id = 1
for i in article_list:
    
    with urllib.request.urlopen(i[0]) as response:
       article = response.read()
    article_soup = BeautifulSoup(article, 'html.parser')
    ps = article_soup.findAll("p", class_=False)
    text = ""
    for p in ps:
        text += p.text
    article_data = {  
        "link": i[0],
        "date": article_soup.find("meta", {"name" : "date"})["content"],
        "keywords": article_soup.find("meta", {"name" : "news_keywords"})["content"],
        "author": article_soup.find("meta", {"name" : "author"})["content"],
        "title": i[1],
        "description": article_soup.find("meta", {"name" : "description"})["content"],
        "text": text
    }
    data[article_id] = article_data
    print("Artikel", article_id, "hinzugefügt")
    article_id += 1 
    if article_id == 100:
        break
    t.sleep(1)

# save data into utf-8 json
with open('data.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)

