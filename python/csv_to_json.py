import pandas as pd

def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file using Pandas
    df = pd.read_csv(csv_file_path)

    # Convert the DataFrame to JSON and save it to a file
    df.to_json(json_file_path, orient='records')

# Specify the file paths
csv_file_path = './short_filtered_file.csv'
json_file_path = 'Movies.json'

# Call the function to convert CSV to JSON
csv_to_json(csv_file_path, json_file_path)

print("CSV file converted to JSON successfully!")