import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
import dotenv

dotenv.load_dotenv()


class Scraper:
    """
    A class to scrape clinical trial data from a given website.
    """

    BASE_URL = os.getenv("BASE_URL")
    SEARCH_URL = (
        BASE_URL + "?term={}&filter=pubt.randomizedcontrolledtrial&sort=date&size=10"
    )

    def __init__(self):
        """Initialize the scraper with a requests session."""
        self.session = requests.Session()

    def scrape(self, keyword, num_pages, start_page=1):
        if num_pages <= 0:
            print("Number of pages must be greater than 0.")
            return []
        trials_data = []
        search_url = self.SEARCH_URL.format(keyword)
        total_pages = self.get_total_pages(keyword)
        for page in range(start_page, min(start_page + num_pages, total_pages + 1)):
            try:
                print(f"Scraping page {page}...")
                url = search_url + f"&page={page}"
                response = self.session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                article_links = soup.find_all("a", class_="docsum-title")
                if not article_links:
                    print(f"No articles found on page {page}. Stopping scrape.")
                    break

                for link in article_links:
                    article_url = self.BASE_URL + link["href"]
                    trial_data = self.scrape_article_page(article_url)
                    if trial_data:
                        trials_data.append(trial_data)
                    else:
                        print("Skipping trial due to scraping failure")
                    time.sleep(random.uniform(0.5, 1))

                print(f"Finished scraping page {page}...")
                time.sleep(random.uniform(2, 3))

            except requests.RequestException as e:
                print(f"Error scraping page {page}: {e}")
                continue
        print(f"Scraped {len(trials_data)} trials successfully.")
        filepath = self.save_scraped_data(trials_data, keyword)
        return filepath

    def scrape_article_page(self, url):
        """
        Scrape an individual article page for title and abstract.

        Args:
            url (str): The URL of the article page.

        Returns:
            dict: A dictionary containing the article's title and abstract.
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.find("h1", class_="heading-title").text.strip()

            abstract_div = soup.find("div", class_="abstract-content selected")
            abstract = (
                abstract_div.text.strip() if abstract_div else "Abstract not available"
            )

            return {"title": title, "abstract": abstract, "url": url}
        except requests.RequestException as e:
            print(f"Network error when accessing {url}: {e}")
        except AttributeError as e:
            print(f"Element not found when scraping article page {url}: {e}")
        except Exception as e:
            print(f"Unexpected error when scraping article page {url}: {e}")

        return None

    def get_total_pages(self, keyword):
        try:
            search_url = self.SEARCH_URL.format(keyword)
            response = self.session.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            results_info = soup.find("div", class_="results-amount")
            if results_info:
                total_results = int(
                    results_info.find("span", class_="value").text.replace(",", "")
                )
                return (total_results + 9) // 10  # 10 results per page
            else:
                print("Couldn't find total results information.")
                return None
        except requests.RequestException as e:
            print(f"Network error when getting total pages: {e}")
        except ValueError as e:
            print(f"Error parsing total results: {e}")
        except Exception as e:
            print(f"Unexpected error when getting total pages: {e}")
        return None

    def save_scraped_data(self, data, keyword):
        script_dir = os.path.dirname(__file__)
        output_dir = os.path.join(script_dir, "../output/scraped-data/")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{keyword.replace(' ', '_')}_scraped_data.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Scraped data saved to {filepath}")
        return filepath
