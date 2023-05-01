import json
from datetime import datetime #convert unix timestamp to readable date

# reads json file
file = open('sample_output.json')
# returns JSON object as a dictionary
data = json.load(file)
# macthes respective id with either its end or start counterpart
# id as key and index of element in json list as value
records_dict = {}
# final summrary of records to write in json file
records_summary = []

# converts timestamps that are not in the 10-digit UNIX format to the one we are working
# it doesnt interfere to the precision of such timestamps
def gets10DigitTime(strTime):
    differenceDigits = len(strTime) - 10
    if differenceDigits < 0:
        decrease = False
    else:
        decrease = True
    differenceDigits = abs(differenceDigits)

    for i in range(differenceDigits):
        if(decrease == True):
            strTime = strTime[:-1]
        else:
            strTime += '0'
    return strTime



for i in range(len(data)):
    currentID = data[i]['id']
    if currentID not in records_dict.keys():
        records_dict[currentID] = i
    else:
        #element to store in summary list
        recordInfo = {}
        indexElement = records_dict[currentID]
        # we are using UNIX timestamp 10 digit which are in seconds and divide them
        # by 60 to obtain hours
        # END AND START TIME
        firstCurrTime = data[i]['timestamp']
        secondCurrTime = data[indexElement]['timestamp']
        if len(firstCurrTime) != 10:
            firstCurrTime = gets10DigitTime(firstCurrTime)
        if len(secondCurrTime) != 10:
            secondCurrTime = gets10DigitTime(secondCurrTime)
        firstCurrTime = int(firstCurrTime)
        secondCurrTime = int(secondCurrTime)
        if data[i]['type'] == 'START':
            recordInfo['SessionStartTime'] = datetime.utcfromtimestamp(firstCurrTime).strftime('%Y-%m-%d %H:%M:%S')
            recordInfo['SessionEndTime'] = datetime.utcfromtimestamp(secondCurrTime).strftime('%Y-%m-%d %H:%M:%S')
        else:
            recordInfo['SessionStartTime'] = datetime.utcfromtimestamp(secondCurrTime).strftime('%Y-%m-%d %H:%M:%S')
            recordInfo['SessionEndTime'] = datetime.utcfromtimestamp(firstCurrTime).strftime('%Y-%m-%d %H:%M:%S')
        # SESSION DURATION
        # converted from UNIX timestamp to hours min and seconds for sessionDuration
        sessionDuration = (abs(secondCurrTime - firstCurrTime))
        hours = sessionDuration // 3600
        hoursDifference = hours
        seconds = sessionDuration % 3600
        minutes = seconds // 60
        seconds = minutes % 60
        hours = str(hours)
        minutes = str(minutes)
        seconds = str(seconds)
        #makes sure that it is represented with clock format when is less than 2 digit for hour/min/sec
        if len(hours) < 2:
            hours = '0' + hours
        if len(minutes) < 2:
            minutes = '0' + minutes
        if len(seconds) < 2:
            seconds = '0' + seconds
        recordInfo['SessionDuration'] = hours + ":" + minutes + ":" + seconds
        # BOOLEAN FLAG indicating if the car was returned later than expected
        if hoursDifference > 24:
            recordInfo['LaterThanExpected'] = True
        else:
            recordInfo['LaterThanExpected'] = False
        # BOOLEAN FLAG indicating if the car was damaged on return
        if data[i]['type'] == 'END':
            if data[i]['comments'] != "":
                recordInfo['DamagedOnReturn'] = True
            else:
                recordInfo['DamagedOnReturn'] = False
        else:
            if data[indexElement]['comments'] != "":
                recordInfo['DamagedOnReturn'] = True
            else:
                recordInfo['DamagedOnReturn'] = False
        records_summary.append(recordInfo)

file.close()

# writes to new json file
with open('summary_final_records.json', 'w') as outfile:
    json.dump(records_summary, outfile,indent=4)

