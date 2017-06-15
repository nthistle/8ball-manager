#!/usr/bin/python
import sys
import fbchat
import getpass
import time

try:
    input = raw_input
except:
    pass

#game constants
k = 150

def getRankings():
    f = open("8ball.dat")
    s = f.read()
    f.close()
    rankingMsg = ""
    i = 1
    for line in s.split("\n"):
        if(len(line)<1):
            continue
        pdat = line.split(",")
        rankingMsg += str(i) + ".)" + (" " * (4-(len(str(i))))) + pdat[0] + ", " + pdat[2] + "\n"
        i += 1
    return rankingMsg    

#handler function to update elos
def updateElo(winnerName, loserName):
    f = open("8ball.dat")
    s = f.read()
    f.close()
    players = []
    for line in s.split("\n"):
        if(len(line)<1):
            continue
        pdat = line.split(",")
        players.append([pdat[0],pdat[1],int(pdat[2])])
    winner = None
    loser = None
    winnerRank = -1
    loserRank = -1
    for p in players:
        #if winnerName.lower() in p[0].lower():
        if p[0].lower().find(winnerName.lower())==0:
            winner = p
            winnerRank = players.index(p)+1
            break
    for p in players:
        #if loserName.lower() in p[0].lower():
        if p[0].lower().find(loserName.lower())==0:
            loser = p
            loserRank = players.index(p)+1
            break
    #print("Winner is " + winnerName + ", loser is " + loserName)
    #print("Identified winner as ",winner)
    #print("Identified loser as ",loser)
    #print("winner is ",winner[2])
    #print("loser is ",loser[2])
    ratingchange = max(5,int(150 / ((10**((winner[2]-loser[2])/400.0))+1)))
    #print("elo change is ",ratingchange)
    #print("")
    retStr = "%s beat %s\n"%(winnerName[0].upper()+winnerName[1:],loserName[0].upper()+loserName[1:])
    retStr += ("%s, %d -> %d (+%d)\n"%(winner[0],winner[2],winner[2]+ratingchange,ratingchange))
    retStr += ("%s, %d -> %d (-%d)\n"%(loser[0],loser[2],loser[2]-ratingchange,ratingchange))
    print(retStr)
    sys.stdout.flush()
    
    winner[2] += ratingchange
    loser[2] -= ratingchange
    f = open("8ball.dat","w")
    players2 = [(-p[2], p[0], p[1]) for p in players]
    players2.sort()
    winnerNew = winner[0]
    loserNew = loser[0]
    nWinnerRank = -1
    nLoserRank = -1
    for p in players2:
        if p[1] == winner[0]:
            nWinnerRank = players2.index(p)+1
        if p[1] == loser[0]:
            nLoserRank = players2.index(p)+1
    if(nWinnerRank == winnerRank):
        retStr += ("%s is still #%d\n" % (winner[0], nWinnerRank))
    else:
        retStr += ("%s rose from #%d to #%d\n" % (winner[0], winnerRank, nWinnerRank))

    if(nLoserRank == loserRank):
        retStr += ("%s is still #%d" % (loser[0], nLoserRank))
    else:
        retStr += ("%s fell from #%d to #%d" % (loser[0], loserRank, nLoserRank))

    for p in players2:
        f.write("%s,%s,%d\n"%(p[1],p[2],-p[0]))
    f.close()
    return retStr


class EightBallBot(fbchat.Client):
    
    def __init__(self,email,password,chatid,debug=True,user_agent=None):
        fbchat.Client.__init__(self,email,password,debug,user_agent)
        self.cid = chatid
	self.send(self.cid, "8-Ball Ranking System now online...", is_user=False)

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)
        if(message.strip() == "/ranking"):
            assert self.send(self.cid, getRankings(), is_user=False)          
        if(message.strip() == "ping"):
            assert self.send(self.cid, "pong", is_user=False)
        try:
            gameMessage = metadata['delta']['messageMetadata']['adminText'].lower().strip().replace("!"," ")
            print("Game Message: " + gameMessage)
            sys.stdout.flush()
            if ("beat" in gameMessage or "lost" in gameMessage) and ("name" not in gameMessage):
                winner = None
                loser = None
                if "beat" in gameMessage:
                    winner = gameMessage.split(" ")[0]
                    loser = gameMessage.split(" ")[2]
                else:
                    winner = gameMessage.split(" ")[3]
                    loser = gameMessage.split(" ")[0]
                retMessage = "Error occurred, check logs"
                try:
                    retMessage = updateElo(winner, loser)
                    print("Elo update successful!")
                except:
                    print("Exception encountered")
                sys.stdout.flush()
                assert self.send(self.cid, retMessage, is_user=False)
                sys.stdout.flush()
            elif "check this out" in gameMessage:
                self.send(self.cid, "Received 'Check this out', please manually input game data", is_user=False)
        except:
            pass

fbchat.log.setLevel(100)

authfile = open("auth.auth")
authraw = authfile.read()
authfile.close()

uid = authraw.split("\n")[0]
pwd = authraw.split("\n")[1]
chatid = authraw.split("\n")[2]

while True:
    try:
        #client = fbchat.Client(uid, pwd)
        print("Launching bot...")
        bot = EightBallBot(uid, pwd, chatid)
        bot.listen()
    except Exception as err:
        print("Received error: ", err)


