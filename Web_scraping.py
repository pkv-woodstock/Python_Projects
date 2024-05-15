# scraping new from hacker news, selecting the title and its link.
# It can scrape data from multiple pages
# Only those news with votes greater than 100 are selected and sorted in decreasing order

from bs4 import BeautifulSoup
import requests
import pprint


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('.titleline')
    subtext = soup.select('.subtext')
    return links, subtext


def sort_stories_by_votes(hnlist):
    sorted_hn = sorted(hnlist, key=lambda k: k['votes'], reverse=True)
    pprint.pprint(sorted_hn)


def extract_data(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].find('a')['href']
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 100:
                hn.append({'title': title, 'link': href, 'votes': points})
    return hn


def main(num_pages):
    base_url = 'https://news.ycombinator.com/news?p='
    all_hn = []
    for page_num in range(1, num_pages + 1):
        links, subtext = scrape_page(base_url + str(page_num))
        hn_data = extract_data(links, subtext)
        all_hn.extend(hn_data)
    sort_stories_by_votes(all_hn)


# base_url = 'https://news.ycombinator.com/news?p='
# original_url = 'https://news.ycombinator.com/news?p=2'
# test_url = base_url + str(2)
# print(original_url == test_url)

if __name__ == "__main__":
    num_pages = int(input(f'Enter the number of pages to scrape'))
    main(num_pages)
