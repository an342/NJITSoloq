import Scales
import sys
import os
import codecs
import threading

#download these with cmd>pip
import urllib3
import certifi
#~~~~~~~~~~~~~~~~~~~~~~~~~~

import json
import time
from random import randint



global players
global conn
global rate
global roles

rate=[0]
players=dict()
roles={"Top":[],"Jungle":[],"Mid":[],"Bot":[],"Support":[]}
conn=urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(),timeout=2.0)
KEY = ""

global teams; teams={}


def checkRate():
    time.sleep(0.1)
def getID(ign):
	try:
		checkRate()
		ign=ign.replace(' ','')
		r=conn.request('GET',"https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/"+ign+"?api_key="+KEY)
		d=json.loads(r.data.decode('utf-8',errors='replace'))
		print(ign+": loaded!")
		return str(d['id'])
	except KeyError as e:
		print(ign,d,e)
def getRank(sid):
    checkRate()
    r=conn.request('GET',"https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/"+sid+"?api_key="+KEY)
    d=json.loads(r.data.decode('utf-8',))
    try:
        tier=d[0]['tier'][0]
        div=d[0]['rank']
        return Scales.ranks[tier+div]
    except KeyError as e:
        print(d)
        #print(e)
        print("defaulting to value of 10")
        return(10)
    except IndexError as e:
        print(e)
        print(d)
        print(Scales.ranks["U"])
        return(Scales.ranks["U"])
def randpop(l):
    return l.pop(randint(0,len(l)-1))
fin=open("list.txt")
lines=fin.readlines()
fin.close()
num=0
for line in lines:
    temp=line.replace('\n,','').lower().split("\t")
    players[num]={}
    players[num]['name']=temp[0]
    players[num]['email']=temp[1]
    players[num]['ign']=temp[2]
    players[num]['id']=getID(temp[2])
    players[num]["Top"]=[0,int(temp[3][0])]
    players[num]["Jungle"]=[0,int(temp[4][0])]
    players[num]["Mid"]=[0,int(temp[5][0])]
    players[num]["Bot"]=[0,int(temp[6][0])]
    players[num]["Support"]=[0,int(temp[7][0])]
    num+=1
del num
for i in players:
    rank=getRank(players[i]['id'])
    for n in roles:
        players[i][n][0]=int(10*rank*players[i][n][1]/Scales.roles[n])
        roles[n]+=[[players[i][n][0],i]]

		
		
roles['Mid']=sorted(roles['Mid']);roles['Mid'].reverse()
roles['Top']=sorted(roles['Top']);roles['Top'].reverse()
roles['Jungle']=sorted(roles['Jungle']);roles['Jungle'].reverse()
roles['Bot']=sorted(roles['Bot']);roles['Bot'].reverse()
roles['Support']=sorted(roles['Support']);roles['Support'].reverse()

def copyRoles():
    temp={}
    for r in roles:
        temp[r]=[]
        for i in range(len(roles[r])):
            temp[r]+=[[roles[r][i][0],roles[r][i][1]]]
        if(roles[r]==temp[r]):
            continue
        else:
            print("ERROR:")
            print(roles[r])
            print("==================")
            print(temp[r])
    if(roles==temp):
        return temp
def sortTeams(num,order):

    team={}
    for i in range(num+1):
        team[i]={"Top":None,"Jungle":None,"Mid":None,"Bot":None,"Support":None}
    troles=copyRoles()
    n=num
    placed=[]
    counter=0
    mod=1
    while(counter<len(players)):
        for r in order:
            print("Team: %s %s %s"%(n,r,players[troles[r][0][1]]['ign']))
            if(team[n][r]==None):
                while(troles[r][0][1] in placed):
                    troles[r].remove(troles[r][0])
                placed+=[troles[r][0][1]]
                team[n][r]=troles[r][0]
                troles[r].remove(troles[r][0])
                counter+=1
            else:
                continue
            if(counter%(num+1)==0):
                if(n==0):
                    mod=0
                elif(n==num):
                    mod=1
            else:
                if(mod and n!=0):
                    n-=1
                elif(n!=num):
                    n+=1
    del troles
    return team

	
def findBest():
	count = 0
	min = 5000
	max = 0
	totalNew = 0
	totalBest = 0
	deltaNew = 5000
	deltaBest = 5000
	
	bestSet = ""
	temp = ""
	fin = open("teams\set.txt")
	setTeams = fin.readlines()
	fin.close()
	for line in setTeams:
		lines=line.replace('\n,','').split("\t")
		
		count = 0
		min = 1200
		max = 0
		
		for i in lines:
			
#			if count > 5:
#				print (int(i[-5:]))

#			elif count > 0:
#				print (int(i[-4:]))
#			else:
#				print (i)
				
			if count > 5:
				print("total:" + i[-5:])
				print("delta: " + str(deltaNew))
			elif count > 0:

				if int(i[-4:]) > max:
					max = int(i[-4:])
					print("NEW MAX: " + str(max))
				elif int(i[-4:]) < min:
					min = int(i[-4:])
					print("NEW MIN: " + str(min))	
				
				deltaNew = max - min
				
				
			elif count == 0:
				temp = i
				print("i: " + i)
				print("temp: " + temp)
			
			count += 1
		if deltaNew < deltaBest:
					
			deltaBest = deltaNew
			print("NEW BEST DELTA: " + str(deltaBest))
			bestSet = temp
			print("NEW BEST SET: " + bestSet)		

			
	print("Best Delta: " + str(deltaBest))
	print ("Use: " + bestSet )
		
	
	
	
	
	
	
orders=[]
c=0
while(c<120):
    troles=list(roles.keys())
    temp=[randpop(troles),randpop(troles),randpop(troles),randpop(troles),randpop(troles)]
    if(temp not in orders):
        orders+=[temp]
        c+=1
for o in range(len(orders)):
    print("Sorting set%s"%(o))
    teams[o]=sortTeams(int(len(players)/5)-1,orders[o])

#END CODE print outs
set=open('.\\teams\set.txt','w')
sets={}
for i in teams:
    fout=open('.\\teams\set%s.txt'%i,'w')
    setTotal=0
    if(i<10):
        set.write('Set #00%s'%(i))
    elif(i<100):
        set.write('Set #0%s'%(i))
    else:
        set.write('Set #%s'%(i))
    for k in teams[i]:
        fout.write("Team %s:\t"%k)
        total=0
        for n in teams[i][k]:
            fout.write(n+": "+players[teams[i][k][n][1]]['ign']+' {'+str(teams[i][k][n][0])+'}\t')
            total+=teams[i][k][n][0]
        if(total<1000):
            fout.write('0%s\n'%total)
            set.write('\tTeam %s: 0%s'%(k,total))
        else:
            fout.write('%s\n'%total)
            set.write('\tTeam %s: %s'%(k,total))
        setTotal+=total
    set.write('\t Set Total:%s\n'%(setTotal))
    fout.close()
set.close()
fout=open('players.txt','w')
for i in players:
    fout.write(players[i]['ign']+'\t'+players[i]['email']+'\t'+players[i]['name']+'\t'+players[i]['id']+'\t'+'Mid: '+str(players[i]['Mid'])+'\t'+'Bot'+str(players[i]['Bot'])+'\t'+'Top'+str(players[i]['Top'])+'\t'+'Jungle'+str(players[i]['Jungle'])+'\t'+'Support'+str(players[i]['Support'])+'\n')
fout.close()

findBest()
