
# Specify the initial page to crawl
seed_item = 'sample_wiki/A12_scale'

seed_url = base_url + seed_item
page = requests.get(seed_url)
soup = bs4.BeautifulSoup(page.text, 'html.parser')

visited = {}
visited[seed_url] = True
pages_visited = 1
print(seed_url)

# Remove index.html to avoid self loops
links = soup.findAll('a')

# Search for all links that lead to "index.html", sotring them as the seed link
seed_link = soup.findAll('a', href=re.compile("^index.html"))

to_visit_realtive = [l for l in links if l not in seed_link and "href" in l.attrs]