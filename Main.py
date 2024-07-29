import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging
import argparse
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
BASE_URL = "https://www.lakmeindia.com"
OUTPUT_CSV = 'lakme_products.csv'


def get_html_content(url: str) -> Optional[str]:
    """Fetch the HTML content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None


def parse_categories(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """Parse and return the list of product categories and their URLs."""
    category_tags = soup.find_all('a', class_=re.compile(r'ctsm_headinglink[1-5]'))
    categories = []
    for tag in category_tags[:5]:
        categories.append({
            'name': tag.text.strip(),
            'url': BASE_URL + tag['href']
        })
    return categories


def parse_product_info(content: BeautifulSoup, category: str) -> List[Dict[str, Optional[str]]]:
    """Parse and return product information from the HTML content."""
    products = []
    product_info = content.find_all('div', class_="ProductItem__Wrapper")

    for product in product_info:
        name = product.find('h2').find('a').text.strip()

        if product.find('span', class_=re.compile(r'\bProductItem__Price 3\b')) is None:
            price = product.find('span', class_="ProductItem__Price Price--highlight 7 Price Text--subdued").text.strip()
        else:
            price = product.find('span', class_=re.compile(r'\bProductItem__Price 3\b')).text.strip()

        if product.find('div', class_='rating__stars') is None:
            rating = None
        else:
            rating = product.find('div', class_='rating__stars').find('span').text

        products.append({
            'Category': category,
            'Name': name,
            'Price': price,
            'Rating': rating
        })

    return products


def main(output_csv: str):
    """Main function to scrape product information and save it to a CSV file."""
    # Fetch and parse the main page
    html_content = get_html_content(BASE_URL)
    if not html_content:
        logging.error("Failed to retrieve the main page.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # Get categories
    categories = parse_categories(soup)
    logging.info(f"Categories found: {[category['name'] for category in categories]}")

    # Collect all product information
    all_products = []

    for category in categories:
        category_url = category['url']
        category_name = category['name']

        page_content = get_html_content(category_url)
        if not page_content:
            logging.warning(f"Skipping category {category_name} due to fetch error.")
            continue

        category_soup = BeautifulSoup(page_content, 'html.parser')
        products = parse_product_info(category_soup, category_name)
        all_products.extend(products)
        logging.info(f"Fetched {len(products)} products from {category_name}")

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_products)
    df.to_csv(output_csv, index=False)
    logging.info(f"CSV file '{output_csv}' has been created successfully.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape product information from Lakme India website.")
    parser.add_argument('--output', type=str, default=OUTPUT_CSV, help='Output CSV file path')
    args = parser.parse_args()
    main(args.output)
