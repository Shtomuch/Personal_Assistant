from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json

class Command(BaseCommand):
    help = 'Scrape news and save to JSON file'

    def handle(self, *args, **kwargs):
        def scrape_news(url, base_url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_items = []
            for item in soup.select('.gc__title a'):
                title = item.text.strip()
                link = base_url + item['href']
                news_items.append({'title': title, 'link': link})

            return news_items

        def save_to_json(data, filename):
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        urls = {
            'economy': "https://www.aljazeera.com/economy/",
            'science-and-technology': "https://www.aljazeera.com/tag/science-and-technology/",
            'football': "https://www.aljazeera.com/tag/football/"
        }

        base_url = 'https://www.aljazeera.com'
        categorized_news = {}

        for category, url in urls.items():
            news_items = scrape_news(url, base_url)
            categorized_news[category] = news_items

        save_to_json(categorized_news, 'utils/categorized_news.json')

        self.stdout.write(self.style.SUCCESS('Successfully scraped news and saved to JSON file'))