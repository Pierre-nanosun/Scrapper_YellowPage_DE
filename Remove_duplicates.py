import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'scraped_data_combined.csv'  # Adjust the path if necessary
df = pd.read_csv(file_path)

# Group by 'Company Name' and aggregate the regions and other fields
df_combined = df.groupby('Company Name').agg({
    'Entry ID': 'first',  # Keep the first entry ID
    'Industry': 'first',  # Keep the first industry (if same across duplicates)
    'Address': 'first',  # Keep the first address
    'Phone': 'first',  # Keep the first phone
    'Website': 'first',  # Keep the first website
    'Email Link': 'first',  # Keep the first email link
    'Partner Level': 'first',  # Keep the first partner level
    'Opening Hours': 'first',  # Keep the first opening hours
    'Region': lambda x: ', '.join(sorted(set(x)))  # Combine regions into a single entry
}).reset_index()

# Save the cleaned DataFrame to a new CSV file
output_file_path = 'scraped_data_combined_cleaned.csv'
df_combined.to_csv(output_file_path, index=False)
