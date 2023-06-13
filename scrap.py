from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import time
import os
import validators
from urllib.parse import urlparse

def getSongs(playlist_url='', playlist_id=''):
    if playlist_url == '':
        playlist_url = f'https://music.amazon.in/user-playlists/{playlist_id}'
        if playlist_id == '':
            return set()

    options = ChromeOptions()
    options.add_argument('--disable-extensions')
    # options.add_argument('--headless')
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')  # Assumes chromedriver is in the same directory as the script file
    print("Getting the songs from url....")
    if not validators.url(playlist_url):
        print("Invalid playlist URL or domain is not supported.")
        return set()

    parsed_url = urlparse(playlist_url)
    if parsed_url.netloc != 'music.amazon.in':
        print("Invalid playlist URL or domain is not supported.")
        return set()


    driver = Chrome(executable_path=chromedriver_path, options=options)

    driver.get(playlist_url)

    # Wait for the page to fully render
    driver.implicitly_wait(10)

    # Extract the HTML content of the visible portion of the page
    html = driver.execute_script("return document.documentElement.outerHTML")

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Extract the song names, artists, and durations from the parsed HTML
    songs_data = set()

    last_count = 0

    time.sleep(5)
    # Simulate scrolling down the page to load more content
    while True:
        soup = BeautifulSoup(html, 'html.parser')
        for song in soup.find_all('div', class_='content'):
            # Extract song title
            title = song.find('div', class_='col1').text.strip()

            # Extract artist name
            artist = song.find('div', class_='col2').text.strip()

            # Extract song duration
            duration = song.find('div', class_='col4').text.strip()

            # Append song data to the list
            songs_data.add((title, artist, duration))

        driver.execute_script("window.scrollBy(0, window.innerHeight - window.innerHeight/20);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        time.sleep(0.1)
        html = driver.execute_script("return document.documentElement.outerHTML")
        if(last_count !=0 and len(songs_data) == last_count):
            break
        last_count = len(songs_data)
    return songs_data