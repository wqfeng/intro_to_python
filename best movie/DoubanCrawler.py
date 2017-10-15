
# __*__ coding: utf-8 __*__
import csv
import requests
import expanddouban
from bs4 import BeautifulSoup

url_prefix = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,"

class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

def getMovieUrl(category, location):
    """
    return a string corresponding to the URL of douban movie lists given category and location.
    """
    url = url_prefix + category + "," + location

    return url

def getHtml(url):
    return expanddouban.getHtml(url, loadmore=True)

def getMovies(category, location):
    """
    return a list of Movie objects with the given category and location.
    """
    url = getMovieUrl(category, location)
    html_doc = getHtml(url)

    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('a', 'item')
    movies = []
    for item in items:
        name = item.find('span', 'title').string
        rate = item.find('span', 'rate').string
        info_link = item['href']
        cover_link = item.find('img')['src']

        movies.append(Movie(name, rate, location, category, info_link, cover_link))

    return movies

def writeToCSV():
    movies = []

    # get categories and locations list
    html_doc = expanddouban.getHtml(url_prefix, loadmore=False)
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('ul', 'category')
    categories_html = list(items[1].children)
    locations_html = list(items[2].children)
    categories = [x.find('span').string for x in categories_html]
    locations = [x.find('span').string for x in locations_html]
    # remove *All*
    categories.pop(0)
    locations.pop(0)

    for c in categories:
        for l in locations:
            movies += getMovies(c, l)
    # movies = getMovies('剧情', '美国')

    with open('movies.csv', 'w', encoding='utf-8') as csvfile:
        movies_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for m in movies:
            movies_writer.writerow([m.name, m.rate, m.location, m.category, m.info_link, m.cover_link])

def caculate():
    html_doc = getHtml(url_prefix) # contains all the movies
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('ul', 'category')

    categories_html = list(items[1].children)
    locations_html = list(items[2].children)
    categories = [x.find('span').string for x in categories_html]
    locations = [x.find('span').string for x in locations_html]
    categories.pop(0)
    locations.pop(0)

    with open('output.txt', 'w', encoding='utf-8') as f:
        for c in categories:
            # will get all the movies in category c when location is empty
            total = len(getMovies(c, ''))
            count_list = []
            for l in locations:
                count_list.append((len(getMovies(c, l)), l))

            count_list.sort(reverse=True)
            first_count, first_location = count_list[0]
            second_count, second_location = count_list[1]
            third_count, third_location = count_list[2]

            f.write('----------------------------------\n')
            f.write('豆瓣共收录{}片 {} 部，数量排名前三的地区为{}、{}、{}，依次占比 {}%、{}%、{}%。\n'.format(
                c, total, first_location, second_location, third_location,
                first_count * 100 / total, second_count * 100 / total, third_count * 100 / total))
            f.write('----------------------------------\n')




if __name__ == '__main__':
    # movies = getMovies('剧情', '美国')
    writeToCSV()
    # caculate()




