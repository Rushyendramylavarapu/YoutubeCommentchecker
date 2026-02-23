# How to Get a YouTube Data API Key

To run this application, you need a YouTube Data API v3 key. Follow these steps to get one for free:

## Step 1: Create a Project in Google Cloud Console
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google account.
3. Click on the project dropdown at the top of the page (it might say "Select a project").
4. Click **"New Project"**.
5. Give your project a name (e.g., "YouTube Sentiment Analyzer") and click **"Create"**.

## Step 2: Enable the YouTube Data API
1. Once your project is created and selected, open the **Navigation Menu** (three lines in the top left).
2. Go to **"APIs & Services"** > **"Library"**.
3. In the search bar, type `YouTube Data API v3` and press Enter.
4. Click on **"YouTube Data API v3"** in the results.
5. Click the blue **"Enable"** button.

## Step 3: Create Credentials (API Key)
1. After enabling the API, click the **"Create Credentials"** button on the top right (or go to **"APIs & Services"** > **"Credentials"**).
2. Click **"+ CREATE CREDENTIALS"** and select **"API key"**.
3. Your new API key will be created and displayed in a popup window.
4. **Copy this key** and save it safely.

## Step 4: Use the Key
1. Run the application:
   ```bash
   python -m streamlit run app.py
   ```
2. Paste the copied API Key into the sidebar input field when the app opens.

> **Note:** This key is private. Do not share it publicly or commit it to GitHub.
