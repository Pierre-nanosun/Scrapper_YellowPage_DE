import os
from bs4 import BeautifulSoup
import pandas as pd
import base64
import re

# Prepare a list to hold the extracted data from all files
all_data = []

# Directory containing the HTML files
directory = "."  # You can set the directory path where the files are located

# Iterate over all files matching the pattern "full_page_[Name].html"
for filename in os.listdir(directory):
    if filename.startswith("full_page_") and filename.endswith(".html"):
        # Extract the region name from the filename
        region = re.search(r"full_page_(.*)\.html", filename).group(1)

        # Load the HTML content from the file
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract all the entries
        entries = soup.find_all('article', class_='mod mod-Treffer')

        # Loop through each entry and extract the required information
        for entry in entries:
            entry_id = entry.get('id')  # Get the article ID

            company_name = entry.find('h2', class_='mod-Treffer__name').get_text(strip=True) if entry.find('h2', class_='mod-Treffer__name') else None
            industry = entry.find('p', class_='mod-Treffer--besteBranche').get_text(strip=True) if entry.find('p', class_='mod-Treffer--besteBranche') else None
            address = entry.find('div', class_='mod-AdresseKompakt__adress-text').get_text(strip=True) if entry.find('div', class_='mod-AdresseKompakt__adress-text') else None
            phone = entry.find('a', class_='mod-TelefonnummerKompakt__phoneNumber').get_text(strip=True) if entry.find('a', class_='mod-TelefonnummerKompakt__phoneNumber') else None

            # Decode the base64 encoded website URL
            website_element = entry.find('span', class_='mod-WebseiteKompakt__text')
            website = None
            if website_element:
                encoded_website_base64 = website_element.get('data-webseitelink')
                if encoded_website_base64:
                    website = base64.b64decode(encoded_website_base64).decode('utf-8')

            # Decode the base64 encoded email link
            email_element = entry.find('span', class_='contains-icon-email gc-btn gc-btn--s')
            email_link = None
            if email_element:
                encoded_email_base64 = email_element.get('data-prg')
                if encoded_email_base64:
                    try:
                        email_link = base64.b64decode(encoded_email_base64).decode('utf-8')
                    except Exception as e:
                        print(f"Error decoding email for entry {entry_id} in {region}: {e}")

            partner_level = entry.find('p', class_='mod-hervorhebungen--partnerHervorhebung').get_text(strip=True) if entry.find('p', class_='mod-hervorhebungen--partnerHervorhebung') else None
            opening_hours = entry.find('div', class_='oeffnungszeitKompakt__text').get_text(strip=True) if entry.find('div', class_='oeffnungszeitKompakt__text') else None

            # Append the extracted data to the list, including the Region
            all_data.append({
                "Entry ID": entry_id,
                "Company Name": company_name,
                "Industry": industry,
                "Address": address,
                "Phone": phone,
                "Website": website,
                "Email Link": email_link,
                "Partner Level": partner_level,
                "Opening Hours": opening_hours,
                "Region": region  # Add the region
            })

            # Debugging information
            #print(f"Processed entry {entry_id} in region {region}: Email link detected: {email_link is not None}")

# Convert the list to a DataFrame
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
df.to_csv("scraped_data_combined.csv", index=False, encoding="utf-8")

print("Scraping completed and data saved to 'scraped_data_combined.csv'.")
