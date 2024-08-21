from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

# Define the search term as a variable
search_term = "photovoltaik"

# Define the list of regions with their respective URLs (using the search term variable)
regions = {
    "Berlin": f"https://www.gelbeseiten.de/branchen/{search_term}/berlin",
    "Hamburg": f"https://www.gelbeseiten.de/branchen/{search_term}/hamburg",
    "Munich": f"https://www.gelbeseiten.de/branchen/{search_term}/muenchen",
    "Cologne": f"https://www.gelbeseiten.de/branchen/{search_term}/koeln",
    "Frankfurt": f"https://www.gelbeseiten.de/branchen/{search_term}/frankfurt am main",
    "Stuttgart": f"https://www.gelbeseiten.de/branchen/{search_term}/stuttgart",
    "Düsseldorf": f"https://www.gelbeseiten.de/branchen/{search_term}/duesseldorf",
    "Dortmund": f"https://www.gelbeseiten.de/branchen/{search_term}/dortmund",
    "Essen": f"https://www.gelbeseiten.de/branchen/{search_term}/essen",
    "Leipzig": f"https://www.gelbeseiten.de/branchen/{search_term}/leipzig",
    "Bremen": f"https://www.gelbeseiten.de/branchen/{search_term}/bremen",
    "Dresden": f"https://www.gelbeseiten.de/branchen/{search_term}/dresden",
    "Hanover": f"https://www.gelbeseiten.de/branchen/{search_term}/hannover",
    "Nuremberg": f"https://www.gelbeseiten.de/branchen/{search_term}/nuernberg",
    "Duisburg": f"https://www.gelbeseiten.de/branchen/{search_term}/duisburg",
    "Bochum": f"https://www.gelbeseiten.de/branchen/{search_term}/bochum",
    "Wuppertal": f"https://www.gelbeseiten.de/branchen/{search_term}/wuppertal",
    "Bielefeld": f"https://www.gelbeseiten.de/branchen/{search_term}/bielefeld",
    "Bonn": f"https://www.gelbeseiten.de/branchen/{search_term}/bonn",
    "Münster": f"https://www.gelbeseiten.de/branchen/{search_term}/muenster",
    "Karlsruhe": f"https://www.gelbeseiten.de/branchen/{search_term}/karlsruhe",
    "Mannheim": f"https://www.gelbeseiten.de/branchen/{search_term}/mannheim",
    "Augsburg": f"https://www.gelbeseiten.de/branchen/{search_term}/augsburg",
    "Wiesbaden": f"https://www.gelbeseiten.de/branchen/{search_term}/wiesbaden",
    "Mönchengladbach": f"https://www.gelbeseiten.de/branchen/{search_term}/moenchengladbach",
    "Gelsenkirchen": f"https://www.gelbeseiten.de/branchen/{search_term}/gelsenkirchen",
    "Braunschweig": f"https://www.gelbeseiten.de/branchen/{search_term}/braunschweig",
    "Kiel": f"https://www.gelbeseiten.de/branchen/{search_term}/kiel",
    "Aachen": f"https://www.gelbeseiten.de/branchen/{search_term}/aachen",
    "Chemnitz": f"https://www.gelbeseiten.de/branchen/{search_term}/chemnitz",
    "Halle": f"https://www.gelbeseiten.de/branchen/{search_term}/halle",
    "Magdeburg": f"https://www.gelbeseiten.de/branchen/{search_term}/magdeburg",
    "Freiburg": f"https://www.gelbeseiten.de/branchen/{search_term}/freiburg",
    "Krefeld": f"https://www.gelbeseiten.de/branchen/{search_term}/krefeld",
    "Lübeck": f"https://www.gelbeseiten.de/branchen/{search_term}/luebeck",
    "Oberhausen": f"https://www.gelbeseiten.de/branchen/{search_term}/oberhausen",
    "Erfurt": f"https://www.gelbeseiten.de/branchen/{search_term}/erfurt",
    "Mainz": f"https://www.gelbeseiten.de/branchen/{search_term}/mainz",
    "Rostock": f"https://www.gelbeseiten.de/branchen/{search_term}/rostock",
    "Kassel": f"https://www.gelbeseiten.de/branchen/{search_term}/kassel",
    "Hagen": f"https://www.gelbeseiten.de/branchen/{search_term}/hagen",
    "Saarbrücken": f"https://www.gelbeseiten.de/branchen/{search_term}/saarbruecken",
    "Hamm": f"https://www.gelbeseiten.de/branchen/{search_term}/hamm",
    "Mülheim": f"https://www.gelbeseiten.de/branchen/{search_term}/muelheim",
    "Potsdam": f"https://www.gelbeseiten.de/branchen/{search_term}/potsdam",
}

# Setup WebDriver options
options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
PROXY = "scrapingant&browser=false:e892fe8b692b4b6db284d680c92e2593@proxy.scrapingant.com:8080"
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument('--proxy-server=%s' % PROXY)

# Loop through each region
for region_name, region_url in regions.items():
    print(f"Processing {region_name}...")

    # Setup WebDriver (make sure the chromedriver or another browser driver is correctly installed)
    driver = webdriver.Chrome(options=options)

    # Open the website for the specific region
    driver.get(region_url)

    # Wait until the "Accept" button is present and clickable
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='cmpboxbtn cmpboxbtnyes cmptxt_btn_yes']"))
        )
        # Click the "Accept" button
        accept_button.click()
        print(f"Accepted the terms and conditions for {region_name}.")
    except Exception as e:
        print(f"Could not find or click the 'Accept' button for {region_name}: {e}")

    # Set the scroll bar to maximum for the search radius
    try:
        slider = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "suchradius_slider"))
        )
        driver.execute_script("arguments[0].value = arguments[0].max;", slider)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)
        print(f"Set the search radius to maximum for {region_name}.")
    except Exception as e:
        print(f"Could not find or set the search radius slider for {region_name}: {e}")

    # Attempt to get total entries at the start
    try:
        total_entries = driver.find_element(By.ID, "loadMoreGesamtzahl").text
    except Exception as e:
        print(f"Could not find the 'total_entries' element for {region_name}. Saving the HTML directly.")
        total_entries = None

    if total_entries:
        while True:
            # Get the current end index
            end_index = driver.find_element(By.ID, "loadMoreGezeigteAnzahl").text

            # Check if all entries have been loaded
            if end_index == total_entries:
                print(f"All entries have been loaded: {end_index} of {total_entries} for {region_name}.")
                break

            print(f"Currently showing {end_index} of {total_entries} entries for {region_name}. Loading more...")

            # Locate the "Load More" button
            load_more_button = driver.find_element(By.ID, "mod-LoadMore--button")

            # Scroll slightly more than the full bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight + 300);")  # Scroll to bottom and slightly more

            # Wait for a random time between 1 and 2 seconds
            time.sleep(random.uniform(1, 2))

            # Move the mouse to the "Load More" button and click
            try:
                actions = ActionChains(driver)
                actions.move_to_element(load_more_button).click().perform()
                print(f"Moved to and clicked the 'Load more' button for {region_name}.")
            except Exception as e:
                print(f"Could not move to or click the 'Load more' button for {region_name}: {e}")
                break  # Exit the loop if the button cannot be clicked

            # Wait for the new content to load
            time.sleep(5)  # Wait for 5 seconds

    # After the loop, or if total_entries was not found, save the full HTML of the page
    html_source = driver.page_source

    # Save the HTML to a file, named by region
    file_name = f"full_page_{region_name}.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_source)

    print(f"Full page HTML for {region_name} saved as '{file_name}'.")

    # Close the browser window for the current region
    driver.quit()

print("Processing completed for all regions.")