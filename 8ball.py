#!/usr/local/bin/python3

def selectplayer(prompt, playerlist):
    print(prompt)
    while(True):
        searchq = input("Search: ").lower()
        if(len(searchq)==0):
            return None # means cancel
        matches = []
        for p in playerlist:
            if p[0].lower().find(searchq)!=-1:
                matches.append(p)
        if(len(matches)==0):
            print("Sorry, no matches were found, please search again")
        elif(len(matches)==1):
            print("Found <" + matches[0][0] + ">, is this correct? (Y/n)")
            inp = input("")
            if len(inp)==0 or inp[0].lower()=="y":
                return matches[0]
        else:
            print("Found %d matches, please be more specific"%len(matches))
            for i in matches:
                print("<%s>"%i[0])

#game constants:
k = 150

## on start, load up data file
print("Loading in player data from 8ball.dat...")
f = open("8ball.dat")
#format:
#Name,pfp-link,elo
#ideally sorted by increasing elo, but will handle that later
players = []
for line in f.read().split("\n"):
    if(len(line)<1):
        continue
    pdat = line.split(",")
    players.append([pdat[0],pdat[1],int(pdat[2])])
print("Player data of %d players loaded"%len(players))
command = "none"
while len(command)>0 and command[0]!="q":
    print("Enter a command:")
    command = input("> ").lower()
    if len(command)==0 or command[0]=="q":
        continue
    if(command[0]=="h"):
        print("===Help Menu===")
        print("display - shows all current player dat")
        print("add - add a new player")
        print("update - add a new game result")
        print("quit")
    elif(command[0]=="d"):
        padsize = max([len(p[0]) for p in players] + [4])+2
        print("Name" + " "*(padsize-4) + "Elo")
        for player in players:
            print(player[0] + " "*(padsize-len(player[0])) + str(player[2]))
    elif(command[0]=="a"):
        nname = input("Name? ")
        npfp = input("Profile Photo Link? ")
        nelo = 1000
        players.append([nname, npfp, nelo])
    elif(command[0]=="u"):
        p1 = selectplayer("Select Player 1", players)
        if p1==None:
            continue
        p2 = selectplayer("Select Player 2", players)
        if p2==None:
            continue
        print("Who won? [1/2]")
        inp = ""
        while inp not in ["1","2"]:
            inp = input("> ")
            if inp not in ["1","2"]:
                print("Please type '1' or '2'")
        # update elo according to formula
        winner = p1 if inp=="1" else p2
        loser = p2 if inp=="1" else p1
        ratingchange = max(5,int(k / ((10**((winner[2]-loser[2])/400))+1)))
        print("%s, %d -> %d"%(winner[0],winner[2],winner[2]+ratingchange))
        print("%s, %d -> %d"%(loser[0],loser[2],loser[2]-ratingchange))
        winner[2] += ratingchange
        loser[2] -= ratingchange
print("Updating player data in 8ball.dat...")
f = open("8ball.dat","w")
players2 = [(-p[2], p[0], p[1]) for p in players]
players2.sort()
for p in players2:
    f.write("%s,%s,%d\n"%(p[1],p[2],-p[0]))
f.close()
print("Done updating data!")
print("Thanks for using 8-ball Rating Manager 1.0")

