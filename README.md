# PubMed Clinical Trial Scraper and Analyzer

This project scrapes clinical trial data from PubMed, processes it using a Large Language Model (LLM), and saves the results to a CSV file.

## Features

- Scrapes clinical trial data from PubMed based on user-specified keywords typed in the terminal.
- Processes the scraped data using the Llama 3.1 70B model via OpenRouter API.
- Parses the LLM response and saves the processed data to a CSV file.
- The script saves intermediate results, allowing for resumption of interrupted scraping sessions.
- Error handling is implemented throughout the script to manage network issues and unexpected data formats.
- The CSV output is structured to facilitate easy analysis of clinical trial data.
- Implements rate limiting and randomized delays to respect PubMed's server load.
- Provides real-time progress updates during the scraping and processing phases.
- Allows users to specify the number of pages to scrape, offering flexibility in data collection.
- Automatically creates necessary directories for storing scraped and processed data.
- Includes a feature to get the total number of available pages for a given search query.
- Offers robust error logging and reporting for easier debugging and maintenance.
- Implements modular design with separate classes for scraping, processing, and data saving, enhancing code maintainability and extensibility.

## Requirements

- Python 3.12.5+
- See `requirements.txt` for Python package dependencies

## Installation

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up your OpenRouter API key in `src/main.py` or in your environment variables(*Recommended*).

## Usage

Run the main script:

```bash
python src/main.py
```

Follow the prompts to enter your search keyword and the number of pages to scrape.

## Project Structure

- `src/main.py`: Main script that orchestrates the scraping, processing, and saving of data
- `src/pubmed_scraper.py`: Contains the `PubMedScraper` class for scraping PubMed
- `src/llm_processor.py`: Contains the `LLMProcessor` class for processing data with the LLM
- `src/data_saver.py`: Contains the `DataSaver` class for saving data to CSV
- `src/prompts.py`: Contains the prompt template for the LLM

## Notes

- This script uses randomized delays between requests to avoid overloading the PubMed server.
- Ensure you comply with PubMed's terms of service and usage guidelines when using this scraper.
- The LLM processing uses the OpenRouter API. Make sure you have sufficient credits and comply with their usage terms.
- Consider the ethical implications of scraping and analyzing medical data, especially regarding patient privacy.
- This tool is intended for research purposes only and should not be used for medical diagnosis or treatment.
- Regular updates may be necessary to maintain compatibility with PubMed's website structure.
- Regular updates may be necessary to maintain compatibility with the LLM model.
- Regular updates may be necessary to maintain compatibility with the OpenRouter API.
- Further debugging my be needed if the LLM is not parsing the data correctly.
- Further debugging my be needed if the data is not being saved to the CSV correctly.
- The script is designed to be run on a single machine with a stable internet connection.

Your Name - [@mrjxtr](https://github.com/mrjxtr)
