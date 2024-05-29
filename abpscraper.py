import requests
from bs4 import BeautifulSoup
import re

def get_news_articles(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    article_links = soup.find_all("a", class_="sub-news-story")
    articles = []

    for article in article_links:
        title = article.find("div", class_="story-title").text.strip()
        article_url = article["href"]
        articles.append((title, article_url))

    return articles

def extract_article_data(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
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
                article_text += p.get_text() + '\n'
            article_text = re.sub(r'<\[^>]+>', '', article_text)
            article_text = article_text.strip()
            return {'title': article_title, 'content': article_text}
        else:
            return {'title': article_title, 'content': "Unable to find the article content on the page."}
    except requests.exceptions.RequestException as e:
        return {'title': None, 'content': f"Error: {e}"}

def get_language_data(languages_urls):
    language_data = []
    for language_url in languages_urls:
        for language, url in language_url.items():
            print(f"Fetching news articles for {language}...")
            news_articles = get_news_articles(url)

            # Iterate through each link and extract article data
            all_article_data = []
            for title, link in news_articles:
                article_data = extract_article_data(link)
                all_article_data.append(article_data)

            language_data.append({"language": language, "articles": all_article_data})

            # Print the data for the current language
            print(f"Language: {language}")
            for article in all_article_data:
                print(f"Title: {article['title']}")
                print(f"Content: {article['content']}")
                print("-" * 30)

    return language_data

# Example usage
languages_urls = [
                  {"marathi": "https://marathi.abplive.com/agriculture"},
                  {"bengali": "https://bengali.abplive.com/agriculture"},
                  {"punjabi": "https://punjabi.abplive.com/news/agriculture"},
                  {"gujarati": "https://gujarati.abplive.com/news/agriculture"},
                  {"telugu": "https://telugu.abplive.com/news/agriculture"},
                  {"tamil": "https://tamil.abplive.com/news/agriculture"},
                  {"english": "https://news.abplive.com/agriculture"},
                  {"hindi": "https://www.abplive.com/agriculture"}
                  ]

if __name__ == "__main__":
    language_data = get_language_data(languages_urls)
