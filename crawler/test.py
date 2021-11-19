import requests
import bs4 as bs
import requests

res = requests.get("https://catalog.gatech.edu/programs/#bachelorstext")
source = bs.BeautifulSoup(res.text, 'lxml')
print(source.find(id="col-content"))

response = requests.get(url)
res = []

source = bs.BeautifulSoup(response.text, 'lxml').find(id="col-content")
if source.find("table") != None and source.find("table").get("class")[0] == 'sc_courselist':
    print("here")
   
for link in source.find_all('a'):
    res.append(url + link.get("href"))

print("here2")