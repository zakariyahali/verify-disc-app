import csv
import json

class DatabaseCleaning():
    """Collection of methods used to clean the dummy csv and convert it to a json & python dictionary format that will be used as dummy Database for this project."""
    def __init__(self):
        pass

    def csv_to_json(self, csv_file, json_file):
        """This method was used to convert a csv file that represents our DB,to a json file."""
        data = []
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)


    def extract_company_names(self, json_data):
        """# -> Two methods to do additional cleaning of data (if needed)"""
        extracted_data = {}
        for obj in json_data:
            company_name = obj["Company Name"]
            del obj["Company Name"]
            extracted_data[company_name] = obj
        return extracted_data

    def extract_company_names_from_json(self):
        """# Load the JSON data from file"""
        with open('C:/Users/Ali/Downloads/python-coding-test-main-tosend/python-coding-test-main/app/database/database.json') as file:
            json_data = json.load(file)

        # Extract company names and create a new JSON
        extracted_json = self.extract_company_names(json_data)

        # Convert the extracted JSON to string
        extracted_json_str = json.dumps(extracted_json, indent=4)

        # Print the extracted JSON
        print(extracted_json_str)

        # Save the extracted JSON to a new file
        with open('database/cleaned_db.json', 'w') as file:
            file.write(extracted_json_str)

    def json_to_dict(self, json_file):
        """This method converts a JSON file to a Python dictionary."""
        with open(json_file) as file:
            data = json.load(file)
        return data
