import xml.etree.ElementTree as ET
import requests
from sendemail import sendEmail
from time import sleep
import datetime


def check_open():
    # course = {'department': 'ECE', 'number': 408, 'crn': 58790}
    # url = 'http://courses.illinois.edu/cisapp/explorer/schedule/2016/fall/{}/{}/{}.xml'.format(course['department'], course['number'], course['crn'])
    # r = requests.get(url)
    # xml = r.text

    # For testing with localXML #
    with open('test.xml', 'r') as xml:
        xml = xml.read()

    try:
        root = ET.fromstring(xml)
    except:
        print "Class doesn't exist :("
        return
    avail = root.find('enrollmentStatus').text
    if avail == "CrossListOpen" or avail == "Open":
        return 1
    elif avail == "CrossListOpen (Restricted)":
        return 1
    else:
        return 0

if __name__ == '__main__':
    print "\n-- FALL 2016 Course Checker by Wayne --\n"
    course_open = 0
    while(1):
        prelog = datetime.datetime.now().strftime("%m/%d %I:%M:%S %p: ")
        if check_open():
            if(course_open != 1):
                sendEmail()
                print "\n{}EMAIL SENT\n".format(prelog)
                course_open = 1
        else:
            print "\n{}closed".format(prelog)
            course_open = 0
        sleep(1260)
