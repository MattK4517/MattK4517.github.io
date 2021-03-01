from flask import Flask, render_template, url_for, request, jsonify
from mySQLControl import mydb, mycursor
import analyze as anlz

app = Flask(__name__)

numRuns = open('runs.txt', mode="r").read()
mycursor.execute("SELECT * FROM ytdata")
myresult = mycursor.fetchall()
normData = []
Data = [] 
for x in myresult:
    normData.append(x)

for x  in range(int(numRuns.splitlines()[-1])):
    Data.append(normData[x + (len(myresult) - int(numRuns.splitlines()[-1])) ])



@app.route("/", methods=["POST", "GET"])
def home():
    artData = []
    vidData = []
    style = ""
    graphType = "songs"
    if request.method == "GET":
        postReq = request.args.get('nm')
        if postReq:
            if postReq == "data" or postReq == "graph":
                titles = []
                for i in range(len(Data)):
                    titles.append(Data[i][1])
                NHTitlesIndex = anlz.artists(titles)[0]
                Artists = anlz.artists(titles)[1]
                actualArtists = anlz.artistAdded(NHTitlesIndex, Artists)
                data = anlz.mostAdded(actualArtists)
                artData = data['Artist']
                vidData = data['videoCount']
                style = "line"
                graphType = "songs"
            else:
                for i in range(len(Data)):
                    if postReq in Data[i][1] or postReq in Data[i][7]:
                        artData.append(Data[i][1])
                        vidData.append(Data[i][2])
                style = "bar"
                graphType = "views"
        return render_template("test.html", content=Data, Artists = artData, Videos = vidData, Style = style, graphType = graphType)
        

    else:
        return render_template("test.html", content=Data, Artists = artData, Videos = vidData, Style = style)


@app.route('/test')
def testing():
    return render_template('formtest.html')

if __name__ == "__main__":
    app.run(debug=True)