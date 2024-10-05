import pandas as pd
import os


class DataSaver:
    """
    A class to save processed clinical trial data to a CSV file.
    """

    def __init__(self):
        self.script_dir = os.path.dirname(__file__)
        self.output_dir = os.path.join(self.script_dir, "../output/csv-data")

    def save_to_csv(self, data, filename):
        """
        Save the processed trial data to a CSV file.

        Args:
            data (list): A list of dictionaries containing processed trial data.
            filename (str): The name of the file to save the data to.

        Raises:
            ValueError: If the data is empty or not in the expected format.
            IOError: If there's an error writing to the file.
        """
        try:
            if (
                not data
                or not isinstance(data, list)
                or not all(isinstance(item, dict) for item in data)
            ):
                raise ValueError(
                    "Invalid data format. Expected a non-empty list of dictionaries."
                )

            df = pd.DataFrame(data)

            # Update the filename to include the output directory
            full_path = os.path.join(self.output_dir, filename)

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            df.to_csv(full_path, index=False)
            print(f"Data successfully saved to {full_path}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except IOError as ioe:
            print(f"Error writing to file {filename}: {ioe}")
        except Exception as e:
            print(f"An unexpected error occurred while saving data: {e}")

    def append_to_csv(self, data, filename):
        """
        Append the processed trial data to an existing CSV file or create a new one if it doesn't exist.

        Args:
            data (list): A list of dictionaries containing processed trial data.
            filename (str): The name of the file to append the data to.

        Raises:
            ValueError: If the data is empty or not in the expected format.
            IOError: If there's an error writing to the file.
        """
        try:
            if (
                not data
                or not isinstance(data, list)
                or not all(isinstance(item, dict) for item in data)
            ):
                raise ValueError(
                    "Invalid data format. Expected a non-empty list of dictionaries."
                )

            df = pd.DataFrame(data)

            # Update the filename to include the output directory
            full_path = os.path.join(self.output_dir, filename)

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Check if file exists and append without header if it does
            if os.path.exists(full_path):
                df.to_csv(full_path, mode="a", header=False, index=False)
                print(f"Data successfully appended to {full_path}")
            else:
                df.to_csv(full_path, index=False)
                print(f"New file created and data saved to {full_path}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except IOError as ioe:
            print(f"Error writing to file {filename}: {ioe}")
        except Exception as e:
            print(f"An unexpected error occurred while saving data: {e}")

    def save_csv_string(self, csv_string, filename):
        """
        Save a CSV string directly to a file using UTF-8 encoding.

        Args:
            csv_string (str): The CSV data as a string.
            filename (str): The name of the file to save the data to.

        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            full_path = os.path.join(self.output_dir, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", newline="", encoding="utf-8") as f:
                f.write(csv_string)
            print(f"Data successfully saved to {full_path}")
        except IOError as ioe:
            print(f"Error writing to file {filename}: {ioe}")
        except Exception as e:
            print(f"An unexpected error occurred while saving data: {e}")

    def save_parsed_data_to_csv(self, parsed_data, filename):
        """
        Save the parsed LLM response data to a CSV file.

        Args:
            parsed_data (dict): A dictionary containing parsed trial data.
            filename (str): The name of the file to save the data to.

        Raises:
            ValueError: If the data is empty or not in the expected format.
            IOError: If there's an error writing to the file.
        """
        try:
            if not parsed_data or not isinstance(parsed_data, dict):
                raise ValueError(
                    "Invalid data format. Expected a non-empty dictionary."
                )

            full_path = os.path.join(self.output_dir, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", newline="", encoding="utf-8") as f:
                for section, data in parsed_data.items():
                    f.write(f"{section}\n")
                    for item in data:
                        f.write(f"{item}\n")
                    f.write("\n")  # Add a blank line between sections

            print(f"Parsed data successfully saved to {full_path}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except IOError as ioe:
            print(f"Error writing to file {filename}: {ioe}")
        except Exception as e:
            print(f"An unexpected error occurred while saving data: {e}")
