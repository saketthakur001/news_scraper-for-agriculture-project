import requests
from bs4 import BeautifulSoup
import re

def abplive_agriculture_links():
    page = requests.get("https://www.abplive.com/agriculture")
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        link_href = link.get('href')
        if "www.abplive.com/agriculture/" in link_href and "www.abplive.com/agriculture/page" not in link_href:
            links.append(link_href)
    return links

def extract_article_data(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # Extract article heading
        heading_div = soup.find('h1')
        if heading_div:
            article_title = heading_div.get_text().strip()
        else:
            article_title = None
        # Extract article content
        article_div = soup.find('div', class_='abp-story-article')
        if article_div:
            article_text = ''
            for p in article_div.find_all('p'):
                article_text += p.get_text() + '\n\n'
            article_text = re.sub(r'<\[^>]+>', '', article_text)
            article_text = article_text.strip()
            return {'title': article_title, 'content': article_text}
        else:
            return {'title': article_title, 'content': "Unable to find the article content on the page."}
    except requests.exceptions.RequestException as e:
        return {'title': None, 'content': f"Error: {e}"}

def get_all_article_data():
    agriculture_links = abplive_agriculture_links()
    all_article_data = []
    for link in agriculture_links:
        article_data = extract_article_data(link)
        all_article_data.append(article_data)
    return all_article_data


if __name__ == '__main__':
    article_data_list = get_all_article_data()
    print(article_data_list)
