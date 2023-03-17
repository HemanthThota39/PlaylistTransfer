from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

playlist_id = 'd1b04fabfa6546aa8e8717277fb0e5f6i8n0'

# Replace with the URL of the Amazon Music playlist you want to scrape
playlist_url = f'https://music.amazon.in/user-playlists/{playlist_id}'

# Set up Selenium to use Chrome in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Edge("msedgedriver.exe")

# Load the playlist page
driver.get(playlist_url)

# Wait for the page to fully render
driver.implicitly_wait(10)

# Extract the HTML content of the visible portion of the page
html = driver.execute_script("return document.documentElement.outerHTML")

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Extract the song names from the parsed HTML
song_names = set()
for song in soup.find_all('div', class_='tracklist-name'):
    song_names.append(song.text.strip())

last_count = 0

# soup = BeautifulSoup(html, 'html.parser')
# for song in soup.find_all('div', class_='col1'):
#     song_names.add(song.text.strip())
time.sleep(5)
# Simulate scrolling down the page to load more content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    soup = BeautifulSoup(html, 'html.parser')
    for song in soup.find_all('div', class_='col1'):
        song_names.add(song.text.strip())
    driver.execute_script("window.scrollBy(0, window.innerHeight - window.innerHeight/20);")
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(0.001)
    html = driver.execute_script("return document.documentElement.outerHTML")
    last_height = new_height
    if(last_count !=0 and len(song_names) == last_count):
        break
    last_count = len(song_names)
    # print(song_names)

for song in song_names:
    print(song)

print("\n")
print(len(song_names))