import requests
from prompts import CLINICAL_TRIAL_PROMPT
import json
import os
import re
from dotenv import load_dotenv

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

    def process_trial(self, trial_data):
        prompt = self.create_prompt(trial_data)
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
                        "content": "You are a helpful assistant specialized in analyzing clinical trials.",
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
            print(f"Network error when processing trial with LLM: {str(e)}")
        except KeyError as e:
            print(f"Unexpected response format: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
        return None

    def create_prompt(self, trial_data):
        """
        Create a prompt for the LLM based on the trial data.

        Args:
            trial_data (dict): A dictionary containing the trial title and abstract.

        Returns:
            str: The formatted prompt for the LLM.
        """
        return CLINICAL_TRIAL_PROMPT.format(
            headline=trial_data["title"], body=trial_data["abstract"]
        )

    def process_scraped_data(self, filepath):
        with open(filepath, "r") as f:
            trials_data = json.load(f)

        responses = []
        for trial in trials_data:
            response = self.process_trial(trial)
            if response:
                responses.append(response)

        return responses

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
            "Group Questions": {},
        }

        for trial_number, response in enumerate(responses, 1):
            parsed_trial = self.parse_trial(response)
            trial_info = parsed_trial["TrialInfo"]

            # Add trial identification data
            parsed_data["Trial Identification"].append(
                {
                    "Trial Number": trial_number,
                    "EudraCT/NCT Number": trial_info["NCT"],
                    "Trial Name": trial_info["Name"],
                    "Number of Patients": trial_info["Patients"],
                }
            )

            # Add trial questions data
            trial_questions = {
                "Trial Number": trial_number,
                "NCT Number": trial_info["NCT"],
                "Phase": "NA",
                "Cancer Type": "NA",
                "Cancer Description": "NA",
                "Sponsor": "NA",
                "Novel Findings": "NA",
                "Conclusions": "NA",
                "Unique Information": "NA",
                "Subgroups with Heightened Response": "NA",
            }

            for qa in parsed_trial["QA"]:
                question = qa["Question"].lower()
                if "phase" in question:
                    trial_questions["Phase"] = qa["Answer"]
                elif "cancer type" in question:
                    trial_questions["Cancer Type"] = qa["Answer"]
                elif "describe the cancer" in question:
                    trial_questions["Cancer Description"] = qa["Answer"]
                elif "sponsor" in question:
                    trial_questions["Sponsor"] = qa["Answer"]
                elif "novel findings" in question:
                    trial_questions["Novel Findings"] = qa["Answer"]
                elif "conclusions" in question:
                    trial_questions["Conclusions"] = qa["Answer"]
                elif "unique information" in question:
                    trial_questions["Unique Information"] = qa["Answer"]
                elif "subgroups" in question:
                    trial_questions["Subgroups with Heightened Response"] = qa["Answer"]

            parsed_data["Trial Questions"].append(trial_questions)

            # Add group questions data
            group_questions = []
            for group_number, group in enumerate(parsed_trial["Groups"], 1):
                group_data = {
                    "Group Number": group_number,
                    "Group Type": group["Type"],
                    "Drug": group["Drug"],
                    "Treatment ORR": "NA",
                    "PFS": "NA",
                    "OS": "NA",
                    "Discontinuation %": "NA",
                    "Met Endpoints": "NA",
                    "Cancer Stages": "NA",
                    "Targets": "NA",
                    "Previous Drug Types": "NA",
                    "Drug Resistance": "NA",
                    "Drug Type Resistance": "NA",
                    "Brain Metastases": "NA",
                    "Previous Surgery": "NA",
                    "Advanced Cancer": "NA",
                    "Metastatic Cancer": "NA",
                    "Previously Untreated": "NA",
                    "Previous Specific Drugs": "NA",
                    "Not Previous Specific Drugs": "NA",
                    "Therapy Line": "NA",
                    "Well Tolerated": "NA",
                    "Adverse Reactions": "NA",
                    "Drug Approval": "NA",
                    "Other Efficacy Data": "NA",
                }
                group_questions.append(group_data)

            parsed_data["Group Questions"][f"Trial {trial_number}"] = group_questions

        return parsed_data

    def parse_trial(self, trial_data):
        lines = trial_data.split("\n")
        trial_info = next(
            (line for line in lines if line.startswith("Trial1-Info:")), ""
        )
        trial_info = self.parse_trial_info(trial_info.replace("Trial1-Info:", ""))

        qa_text = "\n".join(lines)
        qa_pairs = self.parse_qa(qa_text)

        groups = [line for line in lines if line.startswith("Group")]
        group_infos = [
            self.parse_group_info(group.split(":", 1)[1])
            for group in groups
            if ":" in group
        ]

        return {"TrialInfo": trial_info, "QA": qa_pairs, "Groups": group_infos}

    def parse_trial_info(self, trial_info):
        parts = trial_info.split(":")
        if len(parts) >= 3:
            return {"NCT": parts[0], "Name": parts[1], "Patients": parts[2]}
        return {"NCT": "NA", "Name": "NA", "Patients": "NA"}

    def parse_group_info(self, group_info):
        parts = group_info.split(":")
        if len(parts) >= 3:
            return {
                "Type": parts[0],
                "Drug": parts[1],
                "Description": ":".join(parts[2:]),
            }
        return {"Type": "NA", "Drug": "NA", "Description": "NA"}

    def parse_qa(self, text):
        qa_pairs = re.findall(
            r"(\w+[-\d]*)\.\s*(.*?)\n\1A\.\s*(.*?)(?=\n\w+[-\d]*\.|\Z)", text, re.DOTALL
        )
        return [{"Question": q.strip(), "Answer": a.strip()} for _, q, a in qa_pairs]

    def _format_trial_data(self, trial_data, group_data):
        formatted_data = []
        # Add trial identification
        formatted_data.append(
            {
                "Section": "Trial Identification",
                **{
                    k: v
                    for k, v in trial_data.items()
                    if k
                    in [
                        "Trial Number",
                        "EudraCT/NCT Number",
                        "Trial Name",
                        "Number of Patients",
                    ]
                },
            }
        )
        # Add trial questions
        formatted_data.append({"Section": "Trial Questions", **trial_data})
        # Add group questions
        for group in group_data:
            formatted_data.append(
                {
                    "Section": f"Group Questions (Trial {trial_data['Trial Number']})",
                    **group,
                }
            )
        return formatted_data

    def format_parsed_data_as_csv(self, parsed_data):
        csv_output = []

        # Trial Identification
        csv_output.append("Trial Identification")
        csv_output.append(
            "Trial Number,EudraCT/NCT Number,Trial Name,Number of Patients"
        )
        for trial in parsed_data["Trial Identification"]:
            csv_output.append(
                f"{trial['Trial Number']},{trial['EudraCT/NCT Number']},{trial['Trial Name']},{trial['Number of Patients']}"
            )
        csv_output.append("")

        # Trial Questions
        csv_output.append("Trial Questions")
        csv_output.append(
            "Trial Number,NCT Number,Phase,Cancer Type,Cancer Description,Sponsor,Novel Findings,Conclusions,Unique Information,Subgroups with Heightened Response"
        )
        for trial in parsed_data["Trial Questions"]:
            csv_output.append(
                f"{trial['Trial Number']},{trial['NCT Number']},{trial['Phase']},{trial['Cancer Type']},{trial['Cancer Description']},{trial['Sponsor']},{trial['Novel Findings']},{trial['Conclusions']},{trial['Unique Information']},{trial['Subgroups with Heightened Response']}"
            )
        csv_output.append("")

        # Group Questions
        for trial_number, groups in parsed_data["Group Questions"].items():
            csv_output.append(f"Group Questions ({trial_number})")
            csv_output.append(
                "Group Number,Group Type,Drug,Treatment ORR,PFS,OS,Discontinuation %,Met Endpoints,Cancer Stages,Targets,Previous Drug Types,Drug Resistance,Drug Type Resistance,Brain Metastases,Previous Surgery,Advanced Cancer,Metastatic Cancer,Previously Untreated,Previous Specific Drugs,Not Previous Specific Drugs,Therapy Line,Well Tolerated,Adverse Reactions,Drug Approval,Other Efficacy Data"
            )
            for group in groups:
                csv_output.append(
                    f"{group['Group Number']},{group['Group Type']},{group['Drug']},{group['Treatment ORR']},{group['PFS']},{group['OS']},{group['Discontinuation %']},{group['Met Endpoints']},{group['Cancer Stages']},{group['Targets']},{group['Previous Drug Types']},{group['Drug Resistance']},{group['Drug Type Resistance']},{group['Brain Metastases']},{group['Previous Surgery']},{group['Advanced Cancer']},{group['Metastatic Cancer']},{group['Previously Untreated']},{group['Previous Specific Drugs']},{group['Not Previous Specific Drugs']},{group['Therapy Line']},{group['Well Tolerated']},{group['Adverse Reactions']},{group['Drug Approval']},{group['Other Efficacy Data']}"
                )
            csv_output.append("")

        return "\n".join(csv_output)
