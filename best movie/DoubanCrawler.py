
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

    with open('movies.csv', 'w', encoding='utf-8') as csvfile:
        movies_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for m in movies:
            movies_writer.writerow([m.name, m.rate, m.location, m.category, m.info_link, m.cover_link])

def test():
    with open('output.txt', 'w', encoding='utf-8') as f:
        with open('movies.csv', 'r', encoding='utf-8') as csvfile:
            records = list(csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL))
            categories = set([x[3] for x in records])
            locations = set([x[2] for x in records])

            for c in categories:
                movies_in_c = [m for m in records if m[3] == c]
                count_by_location = []
                for l in locations:
                    count_by_location.append((l, len([m for m in movies_in_c if m[2] == l])))
                
                sorted_list = sorted(count_by_location, key=lambda x: x[1], reverse=True)
                first_location, first_count = sorted_list[0]
                second_location, second_count = sorted_list[1]
                third_location, third_count = sorted_list[2]
                total = len(movies_in_c)
                print(c)
                print('豆瓣共收录{}片 {} 部，数量排名前三的地区为{}、{}、{}，依次占比 {:.2%}、{:.2%}、{:.2%}。\n'.format(
                    c, total, first_location, second_location, third_location,
                    first_count / total, second_count / total, third_count / total))
            
                f.write('豆瓣共收录{}片 {} 部，数量排名前三的地区为{}、{}、{}，依次占比 {:.2%}、{:.2%}、{:.2%}。\n'.format(
                c, total, first_location, second_location, third_location,
                first_count / total, second_count / total, third_count / total))


if __name__ == '__main__':
    # writeToCSV()
    test()
