# PlaylistTransfer
Creating an application that would transfer playlists accross the music streaming services like prime music, spotify, etc.

## Setup Application
1. Clone the repository

2. Install the libraries mentioned in **requirements.txt** file using this command:
`pip install -r requirements.txt`

3. Create a [spotify developer account](https://developer.spotify.com/dashboard/login), and create a new app in dashboard, name your app whatever you want to.

4. create a `.env` file in the root directory of this cloned repository.

5. Get the following details from dashboard and paste them in your .env file
 
      - `CLIENT_ID=<your client_id here>`
      - `CLIENT_SECRET=<your client_secret here>` 
      - `REDIRECT_URI=<your redirect uri here>`(This should be added in your **DASHBOARD>EDIT_SETTINGS>RedirectURIs**)

6. Download the [chrome webdriver](https://chromedriver.chromium.org/downloads) if you don't have and paste it in the root directory of this application

7. Run this command to use the application `python app.py`

## Instructions

- Once you have logged in with your spotify credentials and accept the terms and conditions, you will be redirected to a page where you can paste your Playlist_url from Amazon Music, and enter what you want to name this playlist.

- Click on transfer button and wait till the process finish (**You can see the progress in terminal window**) and your browser says a success message! 🎉🎉🎉🎉

## Limitations

- As this app is in development mode, you can add only upto 25 users on the same developer account and you have to add new users in `USERS AND ACCESS` menu in your dashboard.

- For now we are supporting only Playlist_URLs from Amazon_music






