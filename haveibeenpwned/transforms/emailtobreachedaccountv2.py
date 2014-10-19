#!/usr/bin/python

import sys
import urllib2
import json

from MaltegoTransform import *

HIBP = "https://haveibeenpwned.com/api/v2/breachedaccount/"  # https://haveibeenpwned.com/API/v2#BreachesForAccount

mt = MaltegoTransform()
mt.parseArguments(sys.argv)
email = mt.getValue()
mt = MaltegoTransform()
getrequrl = HIBP + email

request = urllib2.Request(getrequrl)
request.add_header('User-Agent', 'Maltego-haveibeenpwned')  # https://haveibeenpwned.com/API/v2#UserAgent 
opener = urllib2.build_opener()

try:
    response = urllib2.urlopen(getrequrl)
    data = json.loads(response.read())
    response = data
    maltego_entity_weight = 1
    for breached in response:
        maltego_entity = mt.addEntity("maltego.Domain", breached['Domain'])
        maltego_entity.setWeight(maltego_entity_weight)
        maltego_entity_weight += 1 

except urllib2.URLError, e:  # https://haveibeenpwned.com/API/v2#ResponseCodes
    
    if e.code == 400:
        mt.addUIMessage("The e-mail account does not comply with an acceptable format", messageType="PartialError")

    if e.code == 403:
        mt.addUIMessage("No user agent has been specified in the request", messageType="PartialError")
    
    if e.code == 404:
        UIMessage = email + " could not be found and has therefore not been pwned"
        mt.addUIMessage(UIMessage, messageType="Inform")
        
mt.returnOutput()