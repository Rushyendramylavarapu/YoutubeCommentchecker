from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

class YouTubeClient:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_video_comments(self, video_id, max_results=5300):
        """
        Fetches comments for a given video ID.
        Returns a list of dictionaries containing comment data.
        """
        comments = []
        try:
            # check if comments are disabled or if video exists first? 
            # We'll just try to fetch threads.
            
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, 500), # API limit per page is 100
                textFormat="plainText"
            )
            
            while request and len(comments) < max_results:
                response = request.execute()
                
                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append({
                        'author': comment['authorDisplayName'],
                        'text': comment['textDisplay'],
                        'published_at': comment['publishedAt'],
                        'like_count': comment['likeCount']
                    })
                
                # Check for next page
                if 'nextPageToken' in response and len(comments) < max_results:
                    request = self.youtube.commentThreads().list_next(request, response)
                else:
                    break
                    
        except HttpError as e:
            print(f"An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        return pd.DataFrame(comments)

    def get_video_comments_page(self, video_id, page_token=None, max_results=100):
        """
        Fetches a single page of comments and returns the dataframe and next page token.
        """
        comments = []
        try:
            kwargs = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": min(max_results, 100), # API limit per page is 100
                "textFormat": "plainText"
            }
            if page_token:
                kwargs["pageToken"] = page_token
                
            request = self.youtube.commentThreads().list(**kwargs)
            response = request.execute()
            
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'published_at': comment['publishedAt'],
                    'like_count': comment['likeCount']
                })
            
            # Return the dataframe and the token for the next page
            next_token = response.get('nextPageToken', None)
            return pd.DataFrame(comments), next_token
                
        except HttpError as e:
            print(f"An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            return None, None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None, None
