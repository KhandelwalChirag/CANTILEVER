# CANTILEVER

This project is licensed under the MIT License - see the LICENSE file for details.

# Products Search Application

This project is a web application built with Flask that scrapes product data from the Lakme India website, stores it in a CSV file, and provides search functionality to find products based on user queries.

## Features

- Scrapes product data from the Lakme India website.
- extracts the details of all the products in different categories from various pages
- Stores product data in a CSV file.
- Provides a web interface to search for products.
- Uses fuzzywuzzy for better search recommendations.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

The CSV file for the data is already included. That can be used directly by running app.py. Otherwise you can use dataExtract.py and update the data CSV file. 

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KhandelwalChirag/CANTILEVER.git
   cd CANTILEVER
   pip install -r requirements.txt
   python dataExtract.py
   python app.py


