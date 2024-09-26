# Clinical Trial Data Extractor with LLM Parsing

This project scrapes clinical trial data from a specified website, processes it using a Large Language Model (LLM) via OpenRouter API, and exports the results to a CSV file. Designed for researchers, it simplifies the extraction and analysis of clinical trial data, providing a streamlined, customizable solution.

## Features

- **Customizable Scraping**: Extract clinical trial data based on user-defined keywords entered via the terminal.
- **LLM-Powered Analysis**: Processes scraped data using advanced LLM models through OpenRouter API.
- **CSV Output**: Generates CSV for the trial data processed from the LLM response.
- **Data Control**: Specify the number of pages to scrape, giving control over the data volume.
- **Page Count Detection**: Automatically retrieves the total number of pages for any search query.
- **Automated Directory Setup**: Automatically creates required directories for storing scraped and processed data.
- **Modular Design**: Clean architecture with separate modules for scraping, processing, and saving data, ensuring easy maintenance and scalability.
- **Real-Time Feedback**: Displays live progress updates during both scraping and data processing phases.
- **Error Handling**: Robust error management for network issues, unexpected data formats, and more.

## Requirements

- Python 3.12.5+
- All required packages are listed in `requirements.txt`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mrjxtr/Clinical_Trial_Data_Extractor.git
   cd Clinical_Trial_Data_Extractor
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your OpenRouter API key by adding it to the `.env` file or directly in `src/main.py`.

## Usage

Run the script using:

```bash
python src/main.py
```

You will be prompted to provide a search keyword and specify the number of pages to scrape.

## Project Structure

- `src/main.py`: Main orchestrator for scraping, processing, and saving data.
- `src/scraper.py`: Contains the `Scraper` class for fetching clinical trial data.
- `src/llm_processor.py`: Implements the `LLMProcessor` class, responsible for analyzing data with the LLM.
- `src/data_saver.py`: Saves processed data in CSV format.
- `src/prompts.py`: Houses customizable LLM prompt templates.

## Notes

- **Randomized Delays**: To avoid server overload, requests include randomized delays.
- **Compliance**: Always adhere to the website's terms of service when scraping data.
- **OpenRouter API Usage**: Ensure you have sufficient API credits and follow OpenRouter's usage policies.
- **Ethical Considerations**: Use this tool responsibly and only for research purposes. It is not intended for medical diagnosis or treatment.
- **Maintenance**: Updates may be needed to adapt to changes in the website, LLM models, or API specifications.
- **Debugging**: If issues occur with LLM parsing or CSV saving, additional debugging may be required.
- **Environment**: Ensure a stable internet connection for running the script on a single machine.

> **Important**: The current parser is optimized for "Breast Cancer" search results. You may need to modify the parser to suit other use cases. All intermediate data is stored in the `output/` directory. The parsing code is located in `src/llm_processor.py` with the `parse_llm_response` function.
