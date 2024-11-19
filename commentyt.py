import os
from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your Google Cloud API key
API_KEY = 'AIzaSyBZDpM9J7NQ0HPDueZzfDfa_q46paNA4VE'

user_url= input("Enter yt link:- ")

#fucntion for cinverting url to video_id
def video_id(url):
    index = url.find("=")
    return  url[index + 1 :]


# Replace 'VIDEO_ID' with the ID of the YouTube video you want to download comments from
VIDEO_ID =  video_id(user_url)

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Define the request to retrieve comments
comments_request = youtube.commentThreads().list(
    part='snippet',
    videoId=VIDEO_ID,
    textFormat='plainText',
    maxResults=100,  # Adjust the number of comments to retrieve as needed
)

# Create a list to store the comments
comments = []

# Fetch comments in batches
while comments_request:
    comments_response = comments_request.execute()

    for comment in comments_response['items']:
        text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(text)

    # Continue to the next page of comments if available
    comments_request = youtube.commentThreads().list_next(comments_request, comments_response)

# Specify the path where you want to save the comments to a text file
output_file = '/content/comments.txt'

# Open the file in write mode and save the comments
with open(output_file, 'w', encoding='utf-8') as file:
    for comment in comments:
        file.write(comment + '\n')

print(f'Comments downloaded and saved to {output_file}')