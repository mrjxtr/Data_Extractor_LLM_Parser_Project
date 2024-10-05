import json
import os
import requests
from dotenv import load_dotenv

from prompts import CLINICAL_TRIAL_PROMPT

load_dotenv()


class LLMProcessor:
    """
    A class to process clinical trial data using a Large Language Model (LLM) via OpenRouter API.
    """

    def __init__(self, api_key):
        """
        Initialize the LLMProcessor with the given API key.

        Args:
            api_key (str): The API key for OpenRouter.
        """
        self.api_key = api_key
        self.api_url = os.getenv("OPENROUTER_API_URL")

    def process_trials(self, trials_data):
        """
        Process all trials at once using the LLM.

        Args:
            trials_data (list): A list of dictionaries containing trial data.

        Returns:
            str: The LLM's response for all trials.
        """
        prompt = self.create_prompt(trials_data)
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Title": "Clinical Trial Analyzer",
            }
            data = {
                "model": os.getenv("MODEL"),
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant specialized in analyzing multiple clinical trials at once.",
                    },
                    {"role": "user", "content": prompt},
                ],
            }
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return content
        except requests.Timeout:
            print("The request to the LLM API timed out. Please try again later.")
        except requests.RequestException as e:
            print(f"Network error when processing trials with LLM: {str(e)}")
        except KeyError as e:
            print(f"Unexpected response format: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return None

    def create_prompt(self, trials_data):
        """
        Create a prompt for the LLM based on multiple trials data.

        Args:
            trials_data (list): A list of dictionaries containing trial data.

        Returns:
            str: The formatted prompt for the LLM.
        """
        trials_text = "\n\n".join(
            [
                f"Trial {i+1}:\nHeadline: {trial['title']}\nBody: {trial['abstract']}"
                for i, trial in enumerate(trials_data)
            ]
        )
        return f"{CLINICAL_TRIAL_PROMPT}\n\nAnalyze the following clinical trials:\n\n{trials_text}"

    def process_scraped_data(self, filepath):
        with open(filepath, "r") as f:
            trials_data = json.load(f)

        response = self.process_trials(trials_data)
        return [response] if response else []

    def save_llm_response(self, responses, keyword):
        script_dir = os.path.dirname(__file__)
        output_dir = os.path.join(script_dir, "../output/response-data/")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{keyword.replace(' ', '_')}_llm_response.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(responses, f, indent=2)

        print(f"LLM response saved to {filepath}")
        return filepath

    def parse_llm_response(self, responses):
        parsed_data = {
            "Trial Identification": [],
            "Trial Questions": [],
            "Study Groups": [],
            "Group Questions": [],
        }

        for response in responses:
            lines = response.split("\n")

            # Parse Trial Identification
            trial_count_line = next(
                (line for line in lines if line.startswith("1A.")), ""
            )
            trial_count = (
                trial_count_line.split(".")[-1].strip() if trial_count_line else "NA"
            )
            parsed_data["Trial Identification"].append(
                f"1,How many Clinical Trials are there?,,\n1A,{trial_count},,\n,,,"
            )

            # Parse Trial Info
            for line in lines:
                if line.startswith("Trial"):
                    parts = line.split(":")
                    if len(parts) >= 4:
                        parsed_data["Trial Identification"].append(
                            f'{parts[0]},{parts[1]}," {parts[2]}",{parts[-1]}'
                        )
                    elif len(parts) == 3:
                        parsed_data["Trial Identification"].append(
                            f'{parts[0]},{parts[1]}," {parts[2]}",NA'
                        )
                    else:
                        parsed_data["Trial Identification"].append(
                            f"{parts[0]},NA,NA,NA"
                        )

            # Parse Trial Questions
            trial_questions = []
            for i in range(1, 10):  # Assuming 9 trial questions
                question_line = next(
                    (line for line in lines if line.startswith(f"{i}.")), ""
                )
                answer_line = next(
                    (line for line in lines if line.startswith(f"{i}A.")), ""
                )

                question = (
                    question_line.split(".", 1)[1].strip() if question_line else "NA"
                )
                answer = answer_line.split(".", 1)[1].strip() if answer_line else "NA"

                trial_questions.append(f'{i}," {question}",,\n{i}A," {answer}",,')
            parsed_data["Trial Questions"].extend(trial_questions)

            # Parse Study Groups
            study_groups = [
                line for line in lines if line.startswith("Group") and ":" in line
            ]
            parsed_data["Study Groups"].extend(study_groups)

            # Parse Group Questions
            group_questions = []
            for i in range(1, 25):  # Assuming 24 group questions
                question_line = next(
                    (line for line in lines if line.startswith(f"Group1-{i}.")), ""
                )
                answer_line = next(
                    (line for line in lines if line.startswith(f"Group1-{i}A.")), ""
                )

                question = (
                    question_line.split(".", 1)[1].strip() if question_line else "NA"
                )
                answer = answer_line.split(".", 1)[1].strip() if answer_line else "NA"

                group_questions.append(
                    f'Group1-{i}," {question}",,\nGroup1-{i}A," {answer}",,'
                )
            parsed_data["Group Questions"].extend(group_questions)

        return parsed_data

    def clean_parsed_data(self, parsed_data):
        """
        Remove specified lines from the parsed data.

        Args:
            parsed_data (dict): The parsed data dictionary.

        Returns:
            dict: The cleaned parsed data dictionary.
        """
        # Remove "Trial Identification,NA,NA,NA"
        parsed_data["Trial Identification"] = [
            line
            for line in parsed_data["Trial Identification"]
            if not line.endswith(",NA,NA,NA")
        ]

        # Remove "Trial Questions,NA,NA,NA"
        parsed_data["Trial Questions"] = [
            line
            for line in parsed_data["Trial Questions"]
            if not line.endswith(",NA,NA,NA")
        ]

        # Remove "Group Questions:" and the two lines after it
        study_groups = parsed_data["Study Groups"]
        indices_to_remove = []
        for i, line in enumerate(study_groups):
            if "Group Questions" in line:
                indices_to_remove.extend([i, i + 1, i + 2])

        parsed_data["Study Groups"] = [
            line for i, line in enumerate(study_groups) if i not in indices_to_remove
        ]

        return parsed_data

    def format_parsed_data_as_csv(self, parsed_data):
        # Clean the parsed data before formatting
        cleaned_data = self.clean_parsed_data(parsed_data)

        csv_output = []

        # Trial Identification
        csv_output.append("Trial Identification:,,,")
        csv_output.append(",,,")
        csv_output.extend(cleaned_data["Trial Identification"])
        csv_output.append(",,,")
        csv_output.append(",,,")

        # Trial Questions
        csv_output.append("Trial Questions:,,,")
        csv_output.append(",,,")
        csv_output.extend(cleaned_data["Trial Questions"])
        csv_output.append(",,,")
        csv_output.append(",,,")

        # Study Groups
        csv_output.append("Study Groups:,,,")
        csv_output.append(",,,")
        csv_output.extend(cleaned_data["Study Groups"])
        csv_output.append(",,,")
        csv_output.append(",,,")

        # Group Questions
        csv_output.append("Group Questions:,,,")
        csv_output.append(",,,")
        csv_output.extend(cleaned_data["Group Questions"])

        return "\n".join(csv_output)
