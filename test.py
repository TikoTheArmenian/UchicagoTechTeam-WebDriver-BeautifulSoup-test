import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
from selenium.common.exceptions import TimeoutException

# Set up WebDriver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

keyword = 'snakes'
driver.get(f'https://www.google.com/search?q={keyword}+site:reddit.com')

# Wait for the elements to be present
try:
    elements_present = EC.presence_of_all_elements_located(
        (By.XPATH, '//*[contains(@href, "/r/")]'))
    WebDriverWait(driver, 10).until(elements_present)
except TimeoutException:
    print("Timed out waiting for page to load")

elements = driver.find_elements(By.XPATH, '//*[contains(@href, "/r/")]')
urls = [element.get_attribute('href') for element in elements]

word_count = {}
for url in urls:
    print(f"Scraping {url}")
    driver.get(url)
    time.sleep(random.uniform(2, 5))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Analyze the page (count words in this case)
    for paragraph in soup.find_all('p'):
        words = paragraph.text.split()
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

# Close the driver after the task is done
driver.quit()

# Display the number of pages scraped
print(f"Found {len(urls)} pages to scrape.")

# Sort words by count and display top 10
sorted_words = sorted(word_count.items(),
                      key=lambda x: x[1], reverse=True)[:10]
if sorted_words:
    words, counts = zip(*sorted_words)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Top 10 Words Across Analyzed Reddit Pages')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("No words were found in the scraped pages.")
