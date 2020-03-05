from ipwhois import IPWhois
from pprint import pprint
import socket
import json

def FindByString(resstring):    #Function finding abuse by string of "type": "abuse", "value": "
    str1 = '"';
    str2 = '"type": "abuse", "value": "';
    try:
        abuseplace = resstring.index(str2)+27  # finding abuse email adress
        endabuseplace = resstring.index(str1, abuseplace + 1)  # finding end of abuse email adress
        abusemail = resstring[abuseplace:endabuseplace]  # abuse email adress found
    except ValueError:
        abusemail=FindByMail(resstring)
    return abusemail


def FindByMail(resstring): #Function finds abuse emial adress by searching for abuse@
    #print("Using function")
    str1 = '"';
    str2 = "abuse@";
    abuseplace = resstring.index(str2)  # finding abuse email adress
    endabuseplace = resstring.index(str1, abuseplace + 1)  # finding end of abuse email adress
    abusemail = resstring[abuseplace:endabuseplace]  # abuse email adress found
    return abusemail


# Using readline()
file1 = open('doobrobki.txt', 'r')
count = 0

while True:
    count += 1

    # Get next line from file
    line = file1.readline()

    # if line is empty
    # end of file is reached
    finalstring=''
    if not line:
        break
    domainName=line.strip()
    #print(domainName)
    try:
        ipadresss = (socket.gethostbyname(domainName))  # Getting IP adress for given www
        #print(ipadresss)
        obj = IPWhois(ipadresss)
        results = obj.lookup_rdap(depth=1)  # getting whois info
        resstring = json.dumps(results)  # getting string from results which is a dict

        #print(resstring)           #used for debugging and showing full whois info

        abusemail=FindByString(resstring)

        #print(abusemail)
        finalstring=finalstring+abusemail+' '+domainName+' '+ipadresss
        print(finalstring)
    except socket.error:
        print(domainName+" ERROR_Incorrect_web_adress_given_ERROR")
file1.close()


