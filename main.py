import os
import pandas as pd
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import analyze as anlz
import plotting as pt
from mySQLControl import toDataBase, backup, mydb

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
Numruns = open("runs.txt", mode="r").read()

##prev data [0][n] title
##prev data [1][n] data
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "cred.json"

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
def newApiTest():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtubeAnalytics"
    api_version = "v2"
    client_secrets_file = "why.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube_analytics = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube_analytics.reports().query(
        dimensions="day",
        endDate="2020-12-31",
        filters="isCurated==1",
        ids="channel==MINE",
        metrics="playlistStarts,estimatedMinutesWatched,views,viewsPerPlaylistStart",
        startDate="2016-01-01"
    )
    response = request.execute()
    return response

if __name__ == "__main__":
    cred = open("cred.json", mode="r").read()
    print(cred)
    #backup("localhost", "root", "abc123", 'testing')
    # normData[0] is PrevViews normData[1] is CurrViews
    # normData[2] is PrevLikes normData[3] is CurrLikes
    # normData[4] is PrevDislikes normData[5] is CurrDislikes
    # normData[6] is PrevComments normData[7] is CurrComments
    # normData[8] is Titles normData[9] is ChannelTitles
    ##    sheets = ["Sheet"+str(int(Numruns)-1), "Sheet"+str(Numruns)]
    ##    Sheetdata = pd.read_excel('ytData.xlsx', sheet_name = sheets)
    ##    Changes = anlz.videoChange(Sheetdata["Sheet"+str(int(Numruns)-1)]["Title"], Sheetdata["Sheet"+str(Numruns)]["Title"])
    ##    normData = anlz.normalize(Sheetdata["Sheet"+str(int(Numruns)-1)], Sheetdata["Sheet"+str(Numruns)], Changes[0], Changes[1])
    ##
    ##    viewChange = anlz.viewChange(normData[0], normData[1])
    ##    likeChange = anlz.likeChange(normData[2], normData[3])
    ##    dislikeChange = anlz.dislikeChange(normData[4], normData[5])
    ##    commentChange = anlz.commentChange(normData[6], normData[7])
    ##
    ##    mvIndex = viewChange.index(max(viewChange))
    ##    lIndex = likeChange.index(max(likeChange))
    ##    dlIndex = dislikeChange.index(max(dislikeChange))
    ##    cIndex = commentChange.index(max(commentChange))
    ##
    ##    print(max(viewChange))
    ##    print(max(likeChange))
    ##    print(max(dislikeChange))
    ##    print(max(commentChange))
    ##    print(normData[8][mvIndex])
    ##    print(normData[8][lIndex])
    ##    print(normData[8][dlIndex])
    ##    print(normData[8][cIndex])



    ##    newData = newApiTest() ## personal user Data
    ##    x = []
    ##    y = []
    ##    print(newData)
    ##    print(len(newData))
    ##    print(newData['columnHeaders'])
    ##    print(newData.keys())
    ##    print(anlz.mostWatched(newData))
    ##    pt.plotWatchTime(newData) ## plot daily watch time
    ##    pt.plotListened(newData) ## plot amount of songs listened to
    ##
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
    while j < 25:
        try:
            for i in range(len(vidData['items'])):
                ##                print(vidData['items'][i]['snippet']['title'])
                ##                print(vidData['items'][i]['snippet']['resourceId'])
                ##                print("\n")
                vids.append(vidData['items'][i]['snippet'])
            vidData = listVids(data['items'][8]['id'], auth, vidData['nextPageToken'])
            j += 1
        except KeyError:
            break

    i = 100
    dt = []
    Titles = []
    Views = []
    Likes = []
    Dislikes = []
    Favorites = []
    Comments = []
    channelTitle = []
    thumbnails = []
    videoId = [] 
    pubDate = []
    IDS = []

    j = 0
    calls = 0
    print(len(vids))
    while j < (len(vids)/50):
        setIDS = []
        for i in range(50):
            try:
                setIDS.append(vids[i+(j*50)]['resourceId']['videoId'])
            except IndexError:
                break
        IDS.append(vidInfo(setIDS, auth))
        j += 1

    for i in range((len(IDS))):
        #print(len(IDS[i]['items']))
        for j in range(len(IDS[i]['items'])):
            try:
                #vids[j+(50*i)].keys() = ['publishedAt', 'channelId', 'title', 'description', 'thumbnails',
                #'channelTitle', 'playlistId', 'position', 'resourceId']
                if vids[j+(50*i)]['title'] == "Deleted video":
                    print("deleted")
                    None
                else:
                    #print(IDS[1]['items'][j]['snippet']['channelTitle'])
                    #print(IDS[i]['items'][j+(50*i)]['snippet']['channelTitle'])
                    dt.append([vids[j+(50*i)]['title'], IDS[i]['items'][j]['statistics']['viewCount'], IDS[i]['items'][j]['statistics']['likeCount'],
                                IDS[i]['items'][j]['statistics']['dislikeCount'], IDS[i]['items'][j]['statistics']['favoriteCount'], IDS[i]['items'][j]['statistics']['commentCount'],
                                IDS[i]['items'][j]['snippet']['channelTitle'], IDS[i]['items'][j]['snippet']['thumbnails']['default']['url'], vids[j+(i*50)]['resourceId']['videoId'], IDS[i]['items'][j]['snippet']['publishedAt']])


            except KeyError:
                dt.append([vids[j+(50*i)]['title'], IDS[i]['items'][j]['statistics']['viewCount'], 0, 0, 0, 0, vids[j+(50*i)]['channelTitle'], IDS[i]['items'][j]['snippet']['thumbnails']['default']['url'], vids[j+(i*50)]['resourceId']['videoId'], IDS[i]['items'][j]['snippet']['publishedAt']])


    for i in range(len(dt)):
        Titles.append(dt[i][0])
        Views.append(dt[i][1])
        Likes.append(dt[i][2])
        Dislikes.append(dt[i][3])
        Favorites.append(dt[i][4])
        Comments.append(dt[i][5])
        channelTitle.append(dt[i][6])
        thumbnails.append(dt[i][7])
        videoId.append(dt[i][8])
        pubDate.append(dt[i][9])

    dataDict = {
        "Title": Titles,
        "Views": Views,
        "likes": Likes,
        "dislikes": Dislikes,
        "favorites": Favorites,
        "comments": Comments,
        "channelTitle": channelTitle,
        "thumbnails": thumbnails,
        "videoId": videoId,
        "pubDate": pubDate,
    }


    df = pd.DataFrame(data = dataDict)
    Numruns = len(dataDict['Title'])
    toDataBase("ytdata", df)

    runs = open("runs.txt", mode="a")
    runs.write(str(Numruns)+"\n")
    runs.close()

    # prevData = []
    # for i in range(Numruns):
    #     prevData.append(myresult[i + ( len(myresult)-Numruns )])
    # prevData = pd.DataFrame(data = prevData, columns= ["id", "Title", "Views", "likes", "dislikes", "favorites", "comments", "channelTitle", "thumbnails", "videoId"])
    currData = df
    # Changes = anlz.videoChange(prevData['Title'], currData['Title'])
    # print(Changes)
    # normData = anlz.normalize(prevData, currData, Changes[0], Changes[1])
    # ##
    # ##
    # ##
    # #### This section finds the artist with the most videos in the playlist
    # Titles = anlz.artists(normData[8])
    # NHTitlesIndex = Titles[0]
    # HTitles = Titles[2]
    # NHTitles = []
    # Artists = Titles[1]
    # for i in range(len(NHTitlesIndex)):
    #     NHTitles.append(normData[8][NHTitlesIndex[i]])
    # for i in range(len(NHTitlesIndex)):
    #     actualArtist = normData[9][NHTitlesIndex[i]].split("-")[0]
    #     Artists.append(actualArtist)

    # testing = anlz.mostAdded(Artists)
    # print(testing['Artist'][testing['videoCount'].index(max(testing['videoCount']))] +": " +str(max(testing['videoCount'])))
    # for i in range(len(testing['Artist'])):
    #     print(testing['Artist'][i]+": "+str(testing['videoCount'][i]))
    
