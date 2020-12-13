import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import analyze as anlz
# 4032
# 4068
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
xlsx = pd.ExcelFile('ytData.xlsx')
prevData = pd.read_excel('ytData.xlsx')
#prev data [0][n] title
#prev data [1][n] data
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlists().list(
         part="snippet,contentDetails",
         maxResults=50,
         mine=True,
         )
    response = request.execute()
    return(response, youtube)
    #print(response)

def listVids(Id, youtube, pageToken):
     request = youtube.playlistItems().list(
         part="snippet, id",
         playlistId = Id,
         maxResults = 50,
         pageToken = pageToken
     )
     response = request.execute()
     return response

def vidInfo(Id, youtube):
    Id = ",".join(Id)
    request = youtube.videos().list(
        part= "snippet,contentDetails,statistics",
        id= Id,
        maxResults = 50
        )
    response = request.execute()
##    print(len(response['items']))
##    print(response['items'])
    return response

def delVid(Id, youtube):
    request = youtube.playlistItems().delete(
        id=Id
        )

if __name__ == "__main__":
    data = main()
    auth = data[1]
    data = data[0]
    i = 0
    j = 1
    vids = []
    #keys for data dict - kind etag pageInfo items
    #data['items'] len = 9
    #data['items'][i] keys - kind etag id snippet contentDetails
    #each item is a playlist ive created
    #dict_keys(['publishedAt', 'channelId', 'title', 'description', 'thumbnails', 'channelTitle', 'playlistId', 'position', 'resourceId'])
    #for vidData['items'][i]['snippet']
    #keys for vidInfo - kind etag items pageInfo
    #keys for vidInfo['items'][i] - kind etag id snippet contentDetails statistics

    vidData = listVids(data['items'][8]['id'], auth, "")
    while j < 19:
        try:
            for i in range(len(vidData['items'])):
##                print(vidData['items'][i]['snippet']['title'])
##                print(vidData['items'][i]['snippet']['resourceId'])
##                print("\n")
                vids.append([vidData['items'][i]['snippet']['title'], vidData['items'][i]['snippet']['resourceId']])
            vidData = listVids(data['items'][8]['id'], auth, vidData['nextPageToken'])
            j += 1
        except KeyError:
            break
    i = 100
    dt = []
    IDS = []
    j = 0
    calls = 0
    while j < len(vids)+50:
        
        try:
            setIDS = []
            for i in range(50):
                setIDS.append(vids[i+j][1]['videoId'])
            IDS.append(vidInfo(setIDS, auth))
            j += 50
        except IndexError:
            break
    for i in range((len(IDS))):
        for j in range(len(IDS[i]['items'])+50):
            try:
                dt.append([vids[j+(50*i)][0], IDS[i]['items'][j]['statistics']['viewCount'], IDS[i]['items'][j]['statistics']['likeCount'],
                           IDS[i]['items'][j]['statistics']['dislikeCount'], IDS[i]['items'][j]['statistics']['favoriteCount'], IDS[i]['items'][j]['statistics']['commentCount']])
            except IndexError:
                break
            except KeyError:
                dt.append([vids[j+(50*i)][0], IDS[i]['items'][j]['statistics']['viewCount']])
    df = pd.DataFrame(data = dt, columns =['Title', 'Views', 'Likes', 'Dislikes', 'UserLiked', 'Comments'])
    with pd.ExcelWriter('ytData.xlsx') as writer:
        df.to_excel(writer)
##    print(prevData.keys())
##    print(df.keys())
    viewChange = []
    for i in range(len(df['Views'])):
        viewChange.append(anlz.viewChange(prevData['Views'][i], df['Views'][i]))
        maxChange = max(viewChange)
        if viewChange[i] >= maxChange:
            index = i
    print(df['Title'][index])
    print(maxChange)
