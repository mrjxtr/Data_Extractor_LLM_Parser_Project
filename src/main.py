import sys
from scraper import Scraper
from llm_processor import LLMProcessor
from data_saver import DataSaver
import json
import os
import dotenv

dotenv.load_dotenv()


def main():
    try:
        keyword = input("Enter the keyword to search for (e.g. 'Breast Cancer'): ")
        scraper = Scraper()

        total_pages = scraper.get_total_pages(keyword)
        if total_pages:
            print(f"Total available pages: {total_pages}")
            num_pages = int(
                input(f"Enter the number of pages to scrape (1-{total_pages}): ")
            )
            if num_pages < 1 or num_pages > total_pages:
                raise ValueError(f"Please enter a number between 1 and {total_pages}")
        else:
            num_pages = int(input("Enter the number of pages to scrape: "))

        llm_processor = LLMProcessor(api_key=os.getenv("OPENROUTER_API_KEY"))
        data_saver = DataSaver()

        all_parsed_data = {
            "Trial Identification": [],
            "Trial Questions": [],
            "Group Questions": {},
        }

        batch_size = 10
        for start_page in range(1, num_pages + 1, batch_size):
            end_page = min(start_page + batch_size - 1, num_pages)
            print(f"Scraping pages {start_page} to {end_page}...")

            # Step 1: Scrape data and save to file
            scraped_data_file = scraper.scrape(
                keyword, end_page - start_page + 1, start_page
            )

            with open(scraped_data_file, "r") as f:
                trials_data = json.load(f)

            if not trials_data:
                print("No trial data found in this batch. Continuing to next batch.")
                continue

            # Step 2: Process scraped data with LLM and save response
            print("Processing trials with LLM...")
            llm_responses = llm_processor.process_scraped_data(scraped_data_file)
            print("Saving LLM response...")
            saved_file = llm_processor.save_llm_response(llm_responses, keyword)

            if saved_file:
                print(f"Response saved to: {saved_file}")
            else:
                print("No file was saved.")

            if not llm_responses:
                print("No LLM responses generated. Continuing to next batch.")
                continue

            # Step 3: Parse LLM response
            print("Parsing LLM and saving LLM response...")
            parsed_data = llm_processor.parse_llm_response(llm_responses)

            # Accumulate parsed data
            print("Converting parsed data to CSV...")
            all_parsed_data["Trial Identification"].extend(
                parsed_data["Trial Identification"]
            )
            all_parsed_data["Trial Questions"].extend(parsed_data["Trial Questions"])
            all_parsed_data["Group Questions"].update(parsed_data["Group Questions"])

        # After all batches are processed, format and save the CSV
        if all_parsed_data["Trial Identification"]:
            print("Saving results to CSV file...")
            csv_output = llm_processor.format_parsed_data_as_csv(all_parsed_data)
            csv_filename = f"{keyword.replace(' ', '_')}_clinical_trials_data.csv"
            data_saver.save_csv_string(csv_output, csv_filename)
            print(f"Results saved to {csv_filename}")
        else:
            print("No data to save.")

        print("Done!")

    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
