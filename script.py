#!/usr/bin/python
import sys
import fbchat
import getpass
from threading import Thread
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os

try:
    input = raw_input
except:
    pass

#game constants
k = 150
hours = 24*3
################################################################################################################################

keywords = [" only has the 8 Ball remaining"," missed"," potted"," has","play 8 Ball Pool"," failed"," beat"," lost", " committed"]
users = []
stockpile = 0
bot = None

def getContent(gm):
    for each in keywords:
        if each in gm:
            return each
    return ""

def setupUsers():
    global users
    global stockpile
    try:
        f = open("users.dat")
        if(not os.path.exists("users.dat")):
            a = 1.0/0.0
        s = f.read().strip()
        f.close()
        players = []
        for line in s.split("\n"):
            if(len(line)<1):
                continue
            pdat = line.split(",")
            users.append([pdat[0],int(pdat[1])])
        stockpile = int(open("stockpile.dat").read().strip())
    except:
        print("Creating users.dat")
        f = open("8ball.dat")
        s = f.read()
        f.close()
        players = []
        for line in s.split("\n"):
            if(len(line)<1):
                continue
            pdat = line.split(",")
            users.append([pdat[0].split(" ")[0],0])
        f = open("users.dat", 'w')
        for each in users:
            f.write(str(each[0]) + "," + str(each[1]) + "\n")
        q = open("stockpile.dat", 'w')
        q.write(str(stockpile))
        q.close()
        f.close()

def incrementHours():
    for x in range(len(users)):
        users[x][1] = users[x][1] + 1
    f = open("users.dat", 'w')
    for each in users:
        f.write(str(each[0]) + "," + str(each[1]) + "\n")
    f.close()
    print(users)
    checkForEloAdjust()

def checkForEloAdjust():
    global stockpile
    global hours
    adjustList = []
    for each in users:
        if each[1] > hours:
            adjustList.append(each[0])
    stockpile += len(adjustList) * 2
    q = open("stockpile.dat", 'w')
    q.write(str(stockpile))
    q.close()
    adjustElo(adjustList)


def sortPlayersList(players):
    players3
    players2 = [(-p[2], p[0], p[1]) for p in players]
    players2.sort()
    for p in players2:
        players3.append([p[1],p[2],-p[0]])
    return players3

def adjustElo(list):
    global stockpile
    global bot
    print(list)
    changedPlayers = []
    if(len(list) == 0):
        return
    f = open("8ball.dat")
    players = []
    for line in f.read().split("\n"):
        if(len(line)<1):
            continue
        pdat = line.split(",")
        players.append([pdat[0],pdat[1],int(pdat[2])])
    lastPlace = ""
    goodPlayers = []
    for x in range(len(players)):
        each = players[x]
        if(each[0].split(" ")[0] in list):
            if(each[2]-2 >= 1000):
                changedPlayers.append([each[0], each[2], each[2] - 2])
                each[2] = each[2] - 2
            else:
                changedPlayers.append([each[0], each[2], 1000])
                each[2] = each[2] - (each[2]-1000)
                stockpile -= each[2] - 1000
        else:
            goodPlayers.append(each[0])
    if(len(goodPlayers) > 0):
        for x in range(int(stockpile / len(goodPlayers))):
            for y in range(len(players)):
                each = players[y]
                if(each[0] in goodPlayers):
                    each[2] = each[2] + 1
        stockpile = stockpile % len(goodPlayers)
    q = open("stockpile.dat", 'w')
    q.write(str(stockpile))
    q.close()
    print("Updating player data in 8ball.dat...")
    f = open("8ball.dat","w")
    players2 = [(-p[2], p[0], p[1]) for p in players]
    players2.sort()
    for p in players2:
        f.write("%s,%s,%d\n"%(p[1],p[2],-p[0]))
    f.close()
    print("Done updating data!")
    print("Thanks for using 8-ball Rating Manager 1.0")
    retMsg = "Due to player inactivity, the followings players have been penalized:\n"
    for each in changedPlayers:
        if(each[1] == 1000 and each[2] == 1000):
            retMsg += each[0] + " stayed at 1000\n"
        else:
            retMsg += each[0] + ", " + str(each[1]) + " -> " + str(each[2]) + " (-2)\n"
    retMsg = retMsg.strip()
    bot.send(bot.cid, retMsg, is_user=False)

def checkIfMidnight():
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    return seconds_since_midnight

def loopContinuously():
    global bot
    while bot == None:
        pass
    bot.send(bot.cid, "8-Ball Ranking Multi-threaded System now online...", is_user=False)
    while True:
        #if checkIfMidnight() < 5:
        if (int(round(time.time() * 1000))/(1000*60.0*60.0)).is_integer():
            print("Creating job")
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            scheduler = BlockingScheduler()
            scheduler.add_job(incrementHours, 'interval', hours=1)
            scheduler.start()
            break

#########################################################################################################3

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
            
            #############################################################################################################

            if (" only has the 8 ball remaining" in gameMessage or " missed" in gameMessage or " potted" in gameMessage or " has" in gameMessage or "play 8 ball pool" in gameMessage or " failed" in gameMessage or ((" beat" in gameMessage or " lost" in gameMessage) and ("name" not in gameMessage))):
                target = gameMessage.split(getContent(gameMessage))[0]
                for x in range(len(users)):
                    if(target == users[x][0]):
                        users[x][1] = 0
                f = open("users.dat", 'w')
                for each in users:
                    f.write(str(each[0]) + "," + str(each[1]) + "\n")
                f.close()
            #############################################################################################################
            
        except:
            pass


fbchat.log.setLevel(100)


authfile = open("auth.auth")
authraw = authfile.read()
authfile.close()

uid = authraw.split("\n")[0]
pwd = authraw.split("\n")[1]
chatid = authraw.split("\n")[2]

setupUsers()

#print("Automatic 8-Ball Ranking System Update Script")
#print("Please Login:")
while True:
    try:
        #INSERT YOUR OWN SHIT
        print("Launching thread...")
        t1 = Thread(target = loopContinuously)
        t1.setDaemon(True)
        t1.start()
        print("Launching bot...")
        bot = EightBallBot(uid, pwd, chatid)
        bot.listen()
        #client = fbchat.Client(uid, pwd)
        
        
    except Exception as err:
        print("Received error: ", err)

