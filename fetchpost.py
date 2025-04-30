import requests
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROFILE_POSTS_URL = 'https://graph.facebook.com/me/posts'

def extract_emojis(text):
    """Extract emojis from a given text."""
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # dingbats
                               u"\U000024C2-\U0001F251"
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols
                               u"\U0001FA70-\U0001FAFF"  # Emoji 13.0+
                               u"\U00002600-\U000026FF"  # Misc symbols
                               "]+", flags=re.UNICODE)
    return emoji_pattern.findall(text) if text else []

def fetch_profile_posts(api_key, url=PROFILE_POSTS_URL):
    """
    Fetch profile posts and return them as a dictionary.

    Args:
        api_key (str): Facebook Graph API access token.
        url (str): API endpoint URL. Default is PROFILE_POSTS_URL.

    Returns:
        dict: A dictionary with post creation dates as keys and post details as values.
    """
    params = {'access_token': api_key}
    posts_dict = {}

    while url:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])

            for post in posts:
                post_id = post.get('id', 'No ID')
                message = post.get('message', 'No message')
                created_time = post.get('created_time', 'No creation time')


                emojis = extract_emojis(message)
                emoji_list = ' '.join(emojis) if emojis else 'No emojis'


                posts_dict[created_time] = {
                    'Post ID': post_id,
                    'Message': message,
                    'Emojis': emoji_list
                }


            url = data.get('paging', {}).get('next')
            params = None
        else:
            print(f"❌ Failed to retrieve posts: {response.status_code}")
            print(f"🔍 Error: {response.text}")
            break

    return posts_dict

