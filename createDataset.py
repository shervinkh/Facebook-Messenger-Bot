import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

personName = raw_input('Enter your full name: ')

def getTelegramData():
	responseDictionary = dict() # The key is the other person's message, and the value is my response

        myMessage, otherPersonsMessage = "", ""
        openedFile = open('telegram.txt', 'r').read()
        allMessages = re.split('\[\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}] ', openedFile)
        for message in allMessages:
           match = re.match('(?P<name>\w+ \w+)( .*)?: (?P<message>.*)', message)
           if match:
               name = match.group('name')
               msg = cleanMessage(match.group('message'))
               if name == personName:
                   if otherPersonsMessage:
                       myMessage += msg + ' '
               else:
                   if myMessage and otherPersonsMessage:
                       responseDictionary[otherPersonsMessage] = myMessage
                       myMessage, otherPersonsMessage = "", ""
                   otherPersonsMessage += msg + ' '

        if myMessage and otherPersonsMessage:
            responseDictionary[otherPersonsMessage] = myMessage

	return responseDictionary

def cleanMessage(message):
	# Remove new lines within message
	cleanedMessage = message.replace('\n',' ').lower()
	# Deal with some weird tokens
	cleanedMessage = cleanedMessage.replace("\xc2\xa0", "")
	# Remove punctuation
	cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
	# Remove multiple spaces in message
	cleanedMessage = re.sub(' +',' ', cleanedMessage)
	return cleanedMessage

combinedDictionary = {}
print 'Getting Telegram Data'
combinedDictionary.update(getTelegramData())
print 'Total len of dictionary', len(combinedDictionary)
print 'Saving conversation data dictionary'
np.save('conversationDictionary.npy', combinedDictionary)

conversationFile = open('conversationData.txt', 'w')
for key,value in combinedDictionary.iteritems():
	if (not key.strip() or not value.strip()):
		# If there are empty strings
		continue
   	conversationFile.write(key.strip() + value.strip())

