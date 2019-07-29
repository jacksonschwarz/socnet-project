import numpy as np
import json
import datetime

#the names of accounts that, according to our criterea, are suspected to be bots
example_cases=[
  "Bonzo30507613",
  "JanSchm61866981",
  "ggarcia238",
  "MaeWest52499669",
  "Horam2017",
  "LisaLov80831185",
  "ChrisOBXnc",
  "HULSEYR7", 
  "kjbtazz", 
  "Tko77457444", 
  "godcountryfami2", 
  "BetsyGBJ9328", 
  "MollyV178", 
  "jolady42", 
  "ECK888888",
]



#function and variable for finding the time sicne the Epoch
#FRM STACK OVERFLOW
epoch=datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds()* 1000.0

#A dictionary of arrays, where the times of each tweet in milliseconds are recorded
times={}
#for every account suspected...
for uname in example_cases:
    #opens the user_status JSON file based off of that username
    file=open("user_status_data/"+uname+"_data.json", "r").read()
    #convert that JSON file into a python dictionary
    user_json=json.loads(file)
    print(uname)
    #a list to keep the times in. 
    created_at_times=[]
    #for every status that the user retweeted...
    for status in user_json:
        #Take out the unnecessary times in the "created_at" field
        sanatized=status["created_at"][4:-11]
        #convert that string into a datetime object
        datetime_object = datetime.datetime.strptime(sanatized, '%b %d %H:%M:%S')
        #take the year from 1969(what it was orginally) to 2018.
        datetime_object=datetime_object.replace(year=2018)
        #add the time in milliseconds to the created_at_times list
        created_at_times.append(unix_time_millis(datetime_object))
    #add the sorted list to the array so that it can be differenced in the next lines.
    times[uname]=sorted(created_at_times)

#The average time difference between retweets per account. The key is the account name and the value is the average time difference
avgTimeDiffs={}
#for every user in the above list.
for uname in times.keys():
    #the sum of the differences is set to 0
    differenceSum=0
    #from 1 to the end of the list...
    for i in range(1, len(times[uname])):
        #the difference is i - (i-1) since the list is already sorted. 
        differenceSum+=times[uname][i]-times[uname][i-1]
    #if the list had any times in it at all....
    if(len(times[uname]) > 0):
        #find the average of all of the differences
        avgTimeDiffs[uname]=(differenceSum/len(times[uname]))
        #and convert it to minutes.
        avgTimeDiffs[uname]/=1000.0
        avgTimeDiffs[uname]/=60
                   
print(avgTimeDiffs)

#write the result to a JSON file for further use/storage.
outfile=open("average_tweet_time_diffs.json", "w")

outfile.write(json.dumps(avgTimeDiffs))
        