#Contains function that analyze data from main.py
from mySQLControl import mydb, mycursor
##viewChange = []
##for i in range(len(df['Views'])):
##     viewChange.append(anlz.viewChange(prevData['Views'][i], df['Views'][i]))
##     maxChange = max(viewChange)
##     if viewChange[i] >= maxChange:
##          index = i
##print(df['Title'][index])
##print(maxChange)

def normalize(PrevData, CurrData, Added, Removed):
     PrevTitles = []
     PrevViews = []
     PrevLikes = []
     PrevDislikes = []
     PrevComments = []
     PrevChannelTitles = []

     CurrTitles = []
     CurrViews = []
     CurrLikes = []
     CurrDislikes = []
     CurrComments = []
     CurrChannelTitles = []
     
     for i in range(len(PrevData['Title'])):
          if PrevData['Title'][i] == "Deleted video":
               i += 1
          else:
               PrevTitles.append(PrevData['Title'][i])
               PrevViews.append(PrevData['Views'][i])
               PrevLikes.append(PrevData['likes'][i])
               PrevDislikes.append(PrevData['dislikes'][i])
               PrevComments.append(PrevData['comments'][i])
               PrevChannelTitles.append(PrevData['channelTitle'][i])
               
     for i in range(len(CurrData['Title'])):
          if CurrData['Title'][i] == "Deleted video":
               i += 1
          else:
               CurrTitles.append(CurrData['Title'][i])
               CurrViews.append(CurrData['Views'][i])
               CurrLikes.append(CurrData['likes'][i])
               CurrDislikes.append(CurrData['dislikes'][i])
               CurrComments.append(CurrData['comments'][i])
               CurrChannelTitles.append(CurrData['channelTitle'][i])
               
     if len(Added) > 0:
          for i in range(len(Added)):
               index = CurrTitles.index(Added[i])
               CurrTitles.remove(Added[i])
               CurrViews.pop(index)
               CurrLikes.pop(index)
               CurrDislikes.pop(index)
               CurrComments.pop(index)
               CurrChannelTitles.pop(index)
                                   
               
     if len(Removed) > 0:
          for i in range(len(Removed)):
               index = PrevTitles.index(Removed[i])
               PrevTitles.remove(Removed[i])
               PrevViews.pop(index)
               PrevLikes.pop(index)
               PrevDislikes.pop(index)
               PrevComments.pop(index)
               PrevChannelTitles.pop(index)
               
##     if PrevTitles == CurrTitles:
##          print("same")
##     if len(PrevViews) == len(CurrViews):
##          print("yesssssir")
     return [PrevViews, CurrViews, PrevLikes, CurrLikes,
             PrevDislikes, CurrDislikes, PrevComments, CurrComments, CurrTitles, CurrChannelTitles]
               
##     for i in range(len(CurrTitles)):
##          if CurrTitles[i] not in PrevTitles:
##               print(CurrTitles[i])
     
     
def viewChange(PrevData, CurrData):
     viewChange = []
     for i in range(len(PrevData)):
         viewChange.append(int(CurrData[i]) - int(PrevData[i])) 
     return viewChange

def likeChange(PrevData, CurrData):
     likeChange = []
     for i in range(len(PrevData)):
          likeChange.append(int(CurrData[i]) - int(PrevData[i]))
     return likeChange

def dislikeChange(PrevData, CurrData):
     dislikeChange = []
     for i in range(len(PrevData)):
          dislikeChange.append(int(CurrData[i]) - int(PrevData[i]))
     return dislikeChange

def commentChange(PrevData, CurrData):
     commentChange = []
     for i in range(len(PrevData)):
          commentChange.append(int(CurrData[i]) - int(PrevData[i]))
     return commentChange

def videoChange(PrevData, CurrData):
     ## analyzes user selected PrevData, and most recent CurrData
     ## detects the changes, if a vid is in prev but not curr append Removed
     ## if a vid is in curr but not prev append Added
     Added = []
     Removed = []
     PrevDataTitle = []
     CurrDataTitle = []
     for i in range(len(PrevData)):
          PrevDataTitle.append(PrevData[i])
     for i in range(len(CurrData)):
          CurrDataTitle.append(CurrData[i])
          
     if len(CurrData) > len(PrevData):
          for i in range(len(CurrData)):
               if PrevDataTitle.count(CurrData[i]) == 0:
                    Added.append(CurrData[i])
                    
     elif len(CurrData) < len(PrevData):
          for i in range(len(PrevData)):
               if CurrDataTitle.count(PrevData[i]) == 0:
                    Removed.append(PrevData[i])
                    
     elif len(CurrData) == len(PrevData):
          for i in range(len(CurrData)):
               if PrevDataTitle.count(CurrData[i]) == 0:
                    Added.append(CurrData[i])
               elif CurrDataTitle.count(PrevData[i]) == 0:
                    Removed.append(PrevData[i])

     print("Songs Added: "+str(Added))
     print("Songs Removed: "+str(Removed))
     return [Added, Removed]

def mostWatched(Data):
     return Data['rows'][Data['rows'].index(max(Data['rows']))]
     ## returns the day in which the user watched the most music

def ChangeIndex():
##     for i in range(len(viewChange)):
##          if
     pass

def artists(Titles):
     # Goes Thru Titles and gets the Artist from videos with "-" in their title
     # if no "-" Uses Channel Title
     # returns a list of the no "-" Titles Indexes, the Artists from "-" vidoes and Titles with "-"
     Artists = []
     Htitles = []
     NHtitles = []
     NHtitlesIndex = []
     fuck = []
     Index = 0
     for Title in Titles:
          Title = Title[0]
          if "-" in Title or "–" in Title:
               if "–" in Title: ## < need this because there are 2 different symbols
                    myDict = Title.maketrans("–", "-") ## switching wierd symbol to actual
                    Title = Title.translate(myDict)
               Htitles.append(Title)
               if len(Title.split('-')) > 2:
                    if "Lyric" in Title.split('-')[2].strip(" "):
                         Artist, song = Title.split('-')[0], Title.split('-')[1]
                         Artists.append(Artist)
                         
                    elif Title.split('-')[0][0] == "[":
                         Artist, song = Title.split('-')[1], Title.split('-')[2]
                         Artists.append(Artist)

                    elif len(Title.split('-')[2]) == 0:
                         Artist, song = Title.split('-')[0], Title.split('-')[1]
                         Artists.append(Artist) 
                         
                    else:
                         fuck.append(Title)
               else:
                    Artist, song = Title.split('-')
               Artists.append(Artist)
          else:
               NHtitles.append(Title)
               NHtitlesIndex.append(Index)
          Index += 1
     return [NHtitlesIndex, Artists, Htitles]

def artistAdded(NHTitlesIndex, Artists):
     mycursor.execute("SELECT channelTitle FROM ytdata")
     titles = mycursor.fetchall()
     channelTitle = []
     for x in range(len(NHTitlesIndex)):
          if len(titles[NHTitlesIndex[x]][0].split("-")) > 1:
               if titles[NHTitlesIndex[x]][0].split("-")[1] == " Topic":
                    channelTitle.append(titles[NHTitlesIndex[x]][0].split("-")[0])
          else:
               channelTitle.append(titles[NHTitlesIndex[x]][0])

     for i in range(len(channelTitle)):
          if channelTitle[i].endswith("VEVO"):
               channelTitle[i] = channelTitle[i].replace("VEVO", " ")
          Artists.append(channelTitle[i])
     return Artists
     #Normalizes all the NHTitles ChannelTitles with the already established Artists list

def mostAdded(Artist):
     #Goes thru Artist List
     #Counts # of each Artist in List
     # Returns a dict of Artists and their videoCounts
     mostAdded = []
     NumAdded = []
     for i in range(len(Artist)):
          Artist[i] = Artist[i].strip()
          if Artist[i] not in mostAdded:
               mostAdded.append(Artist[i])
     for i in range(len(mostAdded)):
          NumAdded.append(Artist.count(mostAdded[i]))
     testDict = {
          "Artist": mostAdded,
          "videoCount":  NumAdded
          }
     return testDict

