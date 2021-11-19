import requests
import json
import bs4 as bs
from urllib.parse import urljoin

# BFS crawler to find all degree programs offered by GT

with open("visited.json", "r") as read_file:
    visited = set(json.load(read_file))

with open("queue.json", "r") as read_file:
    queue = list(json.load(read_file))

with open("urls.json", "r") as read_file:
    urls = list(json.load(read_file))

# find all links on first page that contain bs
# and add to queue as a starting point
def find_bs(url):
    response = requests.get(url)
    source = bs.BeautifulSoup(response.text, 'lxml').find(id="col-content")
    
    for link in source.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/') and "-bs" in path:
            queue.append(urljoin(url, path))

# find all links in the page's content
# return whether the given page contains a courselist table 
def find_all_links(url):

    # avoid mailto links
    if url[:4] != "http":
        return [], False

    response = requests.get(url)
    res = []

    source = bs.BeautifulSoup(response.text, 'lxml').find(id="col-content")
    if source == None:
        return res, False
    
    # add only links that reference the current site
    # no outside links
    for link in source.find_all('a'):
        path = link.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
            res.append(path)
        
    # determine whether page contains a valid courselist
    if source.find("table") and source.find("table").get("class") and  source.find("table").get("class")[0] == 'sc_courselist':
        if "-bs" in url:
            return res, True
        else:
            return res, False

    return res, False


if __name__ == "__main__":

    # initialize queue
    if len(queue) == 0:
        find_bs("https://catalog.gatech.edu/programs/#bachelorstext")

    # basic bfs using helper method
    loop_count = 0
    while len(queue) != 0:
        url = queue.pop(0)
        print(url)
        if url not in visited:
            links, valid = find_all_links(url)
            visited.add(url)

            if valid:
                urls.append(url)

            for link in links:
                if link not in visited and link[:6] != "mailto" and "search" not in link:
                    queue.append(link)

        # logic to cache visited sites in case of crawler crash
        loop_count += 1
        if loop_count % 20 == 0:
            with open("queue.json", "w") as write_file:
                json.dump(queue, write_file)

            with open("urls.json", "w") as write_file:
                json.dump(urls, write_file)

            with open("visited.json", "w") as write_file:
                json.dump(list(visited), write_file)

    
