import pandas as pd
import re
import unicodedata

# Load the CSV files into dataframes
scraped_df = pd.read_csv('scraped_data_combined_cleaned.csv')
raynet_df = pd.read_csv('Raynet_accounts_simplified.csv')

# Standardize columns by trimming spaces and converting to lower case
def standardize_column(df, column):
    if column in df.columns:
        df[column] = df[column].astype(str).str.strip().str.lower()

# List of columns to standardize for each dataframe
scraped_columns = ['Company Name', 'Phone', 'Website']
raynet_columns = ['Account Name', 'Phone 1', 'Phone 2', 'Email', 'Email 2', 'WWW']

for col in scraped_columns:
    standardize_column(scraped_df, col)

for col in raynet_columns:
    standardize_column(raynet_df, col)

# Normalize text by removing special characters and accents
def normalize_text(text):
    if pd.notna(text) and len(text.strip()) > 1:
        text = text.strip().lower()
        text = unicodedata.normalize('NFKD', text)  # Normalize Unicode characters
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        return text
    return ''

# Apply normalization
scraped_df['Normalized Company Name'] = scraped_df['Company Name'].apply(normalize_text)
raynet_df['Normalized Account Name'] = raynet_df['Account Name'].apply(normalize_text)

# Function to extract domain from email
def extract_email_domain(email):
    return email.split('@')[-1] if pd.notna(email) and len(email.strip()) > 1 else None

# Function to extract domain from website
def extract_website_domain(website):
    if pd.notna(website) and len(website.strip()) > 1:
        website = re.sub(r'^https?://', '', website)
        return website.split('/')[0]
    return None

# Apply the extraction functions to create new columns
scraped_df['Website Domain'] = scraped_df['Website'].apply(extract_website_domain)
raynet_df['Email Domain'] = raynet_df['Email'].apply(extract_email_domain)
raynet_df['Email 2 Domain'] = raynet_df['Email 2'].apply(extract_email_domain)
raynet_df['Website Domain'] = raynet_df['WWW'].apply(extract_website_domain)

# Drop rows with NaN values in relevant columns to prevent incorrect matches
scraped_df = scraped_df.dropna(subset=['Website Domain'])
raynet_df = raynet_df.dropna(subset=['Website Domain'])

# Normalize columns in raynet_df for consistency in matching
raynet_df['Normalized Account Name'] = raynet_df['Account Name'].apply(normalize_text)

# Function to find duplicates with exact matching and normalized checks
def find_duplicate_account(scraped_row, raynet_df):
    company_name = normalize_text(scraped_row['Company Name'])
    phone = scraped_row['Phone']
    website_domain = scraped_row['Website Domain']

    # Filter out rows with NaN values in comparison columns
    filtered_raynet_df = raynet_df.dropna(subset=['Normalized Account Name', 'Phone 1', 'Phone 2', 'Email Domain', 'Email 2 Domain', 'Website Domain'])

    # Create boolean masks for each condition
    company_match = filtered_raynet_df['Normalized Account Name'] == company_name
    phone_match = (filtered_raynet_df['Phone 1'] == phone) | (filtered_raynet_df['Phone 2'] == phone)
    email_domain_match = (filtered_raynet_df['Email Domain'] == website_domain) | (filtered_raynet_df['Email 2 Domain'] == website_domain)
    website_domain_match = filtered_raynet_df['Website Domain'] == website_domain

    # Combine all the match criteria
    matches = filtered_raynet_df[company_match | phone_match | email_domain_match | website_domain_match]

    # Return the first match if found
    if not matches.empty:
        return matches['Account Name'].values[0]
    return None

# Apply the duplication check
scraped_df['Raynet Duplicate'] = scraped_df.apply(find_duplicate_account, axis=1, raynet_df=raynet_df)

# Save the updated dataframe to a new CSV file
scraped_df.to_csv('scraped_data_combined_cleaned_raynet.csv', index=False)

print("The file has been saved as 'scraped_data_combined_cleaned_raynet.csv' with the new columns for extracted domains and 'Raynet Duplicate'.")
