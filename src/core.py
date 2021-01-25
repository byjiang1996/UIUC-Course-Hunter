import xml.etree.ElementTree as ET
import requests
from sendemail import sendEmail
from time import sleep
import datetime
import os
from pytz import timezone

### Edit the below fields for the courses you want!!! ###

year = '2021'
term = 'spring'
courses = [
    {'department': 'CS', 'number': 423, 'crn': 	31379},
    {'department': 'CS', 'number': 425, 'crn': 	68088},
]

#######################################################

def check_open(department, number, crn):
    url = 'http://courses.illinois.edu/cisapp/explorer/schedule/{}/{}/{}/{}/{}.xml'.format(year, term, department, number, crn)
    r = requests.get(url)
    xml = r.text

    # For testing with localXML #
    # with open('test.xml', 'r') as xml:
    #     xml = xml.read()

    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        print( "Class doesn't exist :(")
        return
    avail = root.find('enrollmentStatus').text
    if avail == "Closed" or avail == "UNKNOWN":
        return 0
    else:
        return 1

if __name__ == '__main__':
    while 1:
        print( 'RUNNNING')
        for course in courses:
            ## book keeping the open status for each course
            if 'open_status' not in course:
                course['open_status'] = False
            
            if check_open(course['department'], course['number'], course['crn']):
                if course['open_status'] == 0:
                    sendEmail("Your class {}-{} has opened.".format(course['department'], course['number']))
                    course['open_status'] = 1
            else:
                if course['open_status'] == 1:
                    sendEmail("Your class has closed")
                course['open_status'] = 0
        sleep(600)
