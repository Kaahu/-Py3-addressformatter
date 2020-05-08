import fileinput

"""
addressformatter.py

A program to check that the email addresses in the InsuroCorp database conform to the
new format requirements (detailed in readme.txt)

@author Mickey Treadwell
"""


# Dictionary of error messages
errorMessage = { 1 : "Too many @ symbols",
                 2 : "Missing \"@\" or \"_at_\"",
                 3 : "Illegal character in mailbox name",
                 4 : "Mailbox name cannot contain two non-alphanumeric characters in a row",
                 5 : "First character of mailbox name must be alphanumeric",
                 6 : "Last character of mailbox name must be alphanumeric",
                 7 : "Domain contains ']' but no '['",
                 8 : "Invalid domain",
                 9 : "Invalid domain IP format",
                 10 : "Domain IP value out of range",
                 11 : "Domain name contains multiple \'_dot_\'s",
                 12 : "domain name contains '_dot_' and also terminates with '.'",
                 13 : "domain name does not terminate in '.' or '_dot_'",
                 14 : "Illegal character in domain name",
                 15 : "First character of domain name must be alphanumeric",
                 16 : "Last character of domain name must be alphanumeric",
                 17 : "Domain name cannot contain multiple '.' in a row",
                 18 : "Domain extension ends in illegal character"}

#Legal delimiters for mailbox name
legalNameChars = ['.', '-', '_']

#Valid non-IP domain extensions
legalDomains = ['co.nz', 'com.au', 'co.ca', 'com', 'co.us', 'co.uk']

#Global variables
error = -1
mailboxName = ""
domainExt = ""
domainName = ""
IPAddress = False
longAt = False

"""
Resets global variables to their defaul values, called after each line.
"""
def reset():

    global error, mailBoxName, domainExt, domainName, IPAddress, longAt
    
    error = -1
    mailboxName = ""
    domainExt = ""
    domainName = ""
    IPAddress = False
    longAt = False

"""
Isolate the name portion of the email address and assign it to a global variable.
"""
def getName(inAddress):

    global mailboxName, error, longAt

    # Check if the given address contains an '@', but not also '_at_'
    if (inAddress.find('@') != -1):
        atIndex = inAddress.find('@')
        if inAddress[atIndex+1:].find('@') != -1:
            error = 1
            return
        elif inAddress[atIndex+1:].find('_at_') != -1:
            error = 1
            return
        mailboxName = inAddress[:atIndex]
        return

    # Check if the given address contains an '_at_', but not also '@'
    elif inAddress.find('_at_') != -1:
        atIndex = inAddress.find('_at_')
        if inAddress[atIndex+1:].find('_at_') != -1:
            error = 1
            return
        elif inAddress[atIndex+1:].find('@') != -1:
            error = 1 # Too many @ symbols
            return
        mailboxName =inAddress[:atIndex]
        longAt = True
        return

    else:
        error = 2 # Missing @ or _at_
        return

"""
Several checks to verify that the mailbox name is valid.
"""
def checkName(inName):
    
    global error, legalNameChars

    # Check if all but the first and last chars of the mailbox name are alphanumeric
    for i in inName[1:-1]:
        if i.isalpha():
            pass
        elif i.isdigit():
            pass
        elif i in legalNameChars:
            pass
        else:
            error = 3 #illegal char in name
            return

    # Check if the mailbox name contains two delimiters in a row
    for i, j in enumerate(inName[:-1]):
        if (j in legalNameChars) & (inName[i+1] in legalNameChars):
            error = 4 # name cannot contain two non-alphanum characters in a row
            return

    # Check that the first character is alphanumeric
    if inName[:1].isalpha():
        pass
    elif inName[:1].isdigit():
        pass
    else:
        error = 5 # first char of name must be alphanumeric
        return

    # Check that the last character is alphanumeric
    if inName[-1].isalpha():
        pass
    elif inName[-1].isdigit():
        pass
    else:
        error = 6 # last char of name must be alphanumeric
        return

"""
Isolate the domain portion of the email address and assign it to a global variable.
"""
def getDomainExt(inAddress):

    global error, domainExt, legalDomains

    for i in legalDomains:
        if inAddress[-len(i):] == i:
            domainExt = i
            return

    if inAddress[-1] == ']':
        if inAddress.find('[') != -1:
            domainExt = inAddress[inAddress.find('['):]
        else:
            error = 7 # Domain contains ] but no [
            return

    else:
        error = 8 # Invalid domain
        return

"""
Verify that the domain is either a legal extension or a valid IP address.
"""
def checkDomainExt(inDomain):

    global error, legalDomains, IPAddress
    
    if inDomain in legalDomains:
        return
    else:
        checkDom = inDomain[1:-1].split('.')
        if len(checkDom) != 4:
            error = 9 # Invalid domain IP format
            return
        for i in checkDom:
            if not i.isdigit():
                error = 9 # Invalid domain IP format
                return
            if 0 <= int(i) <= 255:
                IPAddress = True
            else:
                error = 10 # Domain IP value out of range
"""
Isolate the domain name  of the email address (if it exists) and assign it to a global variable.
"""
def getDomainName(inAddress):

    global error, mailboxName, domainName, domainExt, IPAddress

    # No domain name if the line contains an IP address
    if IPAddress:
        return
    #Isolate the domain from '@' / '_at_'
    else:
        domainName = inAddress[len(mailboxName):len(inAddress)-len(domainExt)]
        if longAt:
            domainName = domainName[4:]
        else:
            domainName = domainName[1:]
            
"""
Determine is the domain name ends in a dot, and that it contains valid characters
"""
def checkDomainName(inDomName):

    global error, domainName, IPAddress

    # Domain name unnecessary if an IP Address is being used
    if IPAddress:
        return
    
    #Check that the domain name terminates with '.' or '_dot_', but not both
    if inDomName[-len('_dot_'):] == '_dot_':
        domainName = inDomName[:len(domainName)-5]
        if '_dot_' in domainName:
            error = 11 # domain name contains multiple '_dot_'s
            return
        
    elif inDomName[-1] == '.':
        domainName = inDomName[:-1]
        if '_dot_' in domainName:
            error = 12 # domain name contains '_dot_' and also terminates with '.'
            return
    else:
        error = 13 # domain name does not terminate in '.' or '_dot_'

    #Check for illegal chars
    for i in domainName[1:-1]:
        if i.isalpha():
            pass
        elif i.isdigit():
            pass
        elif i == '.':
            pass
        else:
            error = 14 #illegal char in domain name
            return

    # Check that first and last chars are alphanumeric
    if domainName[:1].isalpha():
        pass
    elif domainName[:1].isdigit():
        pass
    else:
        error = 15 # first char of domain name must be alphanumeric
        return

    if domainName[-1].isalpha():
        pass
    elif domainName[-1].isdigit():
        pass
    else:
        error = 16 # last char of domain name must be alphanumeric
        return

    #Check for instances of multiple '.' in a row
    for i in domainName[:-1]:
        if (i == '.') & (domainName[domainName.index(i)+1] == '.'):
            error = 17 # domain name contains two '.'s in a row
            return
    
"""
Take lines from standard input, run all checks, print out either the formatted email address
or the unformatted address with the relevant error message
"""

for line in fileinput.input():

    if line[-2].isalpha():
        pass
    elif line[-2] == ']':
        pass
    else:
        error = 18 # Domain extension ends in illegal character
        
    address = line.rstrip()
    
    getName(address.lower())

    if error == -1:
        checkName(mailboxName)

    if error == -1:
        getDomainExt(address.lower())

    if error == -1:
        checkDomainExt(domainExt)

    if error == -1:
        getDomainName(address.lower())

    if error == -1:
        checkDomainName(domainName)

    if error == -1:
        if IPAddress:
            print(mailboxName+'@'+domainExt)
        else:
            print(mailboxName+'@'+domainName+'.'+domainExt)
    else:
        print(address, '<---', errorMessage[error])

    reset()


