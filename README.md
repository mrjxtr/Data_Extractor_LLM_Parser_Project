# CLINICAL TRIAL DATA EXTRACTOR WITH LLM PARSING

## Project Summary 📝

The **Clinical Trial Data Extractor with LLM Parsing** project scrapes clinical trial data from a specified website (which will remain unnamed), processes it using a Large Language Model (LLM) via the OpenRouter API, and exports the results to a CSV file. This tool is designed for researchers, providing a streamlined and customizable solution for extracting and analyzing clinical trial data.

<br />

<div align="center">
  
  [![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mrjxtr)
  [![Upwork](https://img.shields.io/badge/-Upwork-6fda44?style=flat-square&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~01f2fd0e74a0c5055a?mp_source=share)
  [![Facebook](https://img.shields.io/badge/-Facebook-1877F2?style=flat-square&logo=facebook&logoColor=white)](https://www.facebook.com/mrjxtr)
  [![Instagram](https://img.shields.io/badge/-Instagram-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/mrjxtr)
  [![Threads](https://img.shields.io/badge/-Threads-000000?style=flat-square&logo=threads&logoColor=white)](https://www.threads.net/@mrjxtr)
  [![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/mrjxtr)
  [![Gmail](https://img.shields.io/badge/-Gmail-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:mr.jesterlumacad@gmail.com)

</div>

### Report outline 🧾

- [Project Summary](#ProjectSummary)
  - [Report outline](#Reportoutline)
  - [Features](#Features)
  - [Requirements](#Requirements)
  - [Installation](#Installation)
  - [Usage](#Usage)
  - [Project Structure](#ProjectStructure)
    - [Notes](#Notes)

### Features 🚀 <a name="Features"></a>

- **Customizable Scraping**: Extract clinical trial data based on user-defined keywords entered via the terminal.
- **LLM-Powered Analysis**: Process scraped data using advanced LLM models through OpenRouter API.
- **CSV Output**: Generate CSV for trial data processed from the LLM response.
- **Data Control**: Specify the number of pages to scrape, giving control over the data volume.
- **Page Count Detection**: Automatically retrieves the total number of pages for any search query.
- **Automated Directory Setup**: Automatically creates required directories for storing scraped and processed data.
- **Modular Design**: Clean architecture with separate modules for scraping, processing, and saving data.
- **Real-Time Feedback**: Displays live progress updates during scraping and data processing phases.
- **Error Handling**: Robust error management for network issues and unexpected data formats.

### Requirements 💻 <a name="Requirements"></a>

- Python 3.12.5+
- All required packages are listed in `requirements.txt`.

### Installation ⚙️ <a name="Installation"></a>

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

### Usage 🖥 <a name="Usage"></a>

Run the script using:

```bash
python src/main.py
```

You will be prompted to provide a search keyword and specify the number of pages to scrape.

### Project Structure 📂 <a name="ProjectStructure"></a>

- `src/main.py`: Main orchestrator for scraping, processing, and saving data.
- `src/scraper.py`: Contains the `Scraper` class for fetching clinical trial data.
- `src/llm_processor.py`: Implements the `LLMProcessor` class for analyzing data with the LLM.
- `src/data_saver.py`: Saves processed data in CSV format.
- `src/prompts.py`: Houses customizable LLM prompt templates.

#### Notes 📌 <a name="Notes"></a>

- **Randomized Delays**: To avoid server overload, requests include randomized delays.
- **Compliance**: Always adhere to the website's terms of service when scraping data.
- **OpenRouter API Usage**: Ensure you have sufficient API credits and follow OpenRouter's usage policies.
- **Ethical Considerations**: Use this tool responsibly and only for research purposes. It is not intended for medical diagnosis or treatment.
- **Maintenance**: Updates may be needed to adapt to changes in the website, LLM models, or API specifications.
- **Debugging**: If issues occur with LLM parsing or CSV saving, additional debugging may be required.
- **Environment**: Ensure a stable internet connection for running the script on a single machine.

> **Important**: The current parser is optimized for "Breast Cancer" search results. You may need to modify the parser to suit other use cases. All intermediate data is stored in the `output/` directory. The parsing code is located in `src/llm_processor.py` with the `parse_llm_response` function.
