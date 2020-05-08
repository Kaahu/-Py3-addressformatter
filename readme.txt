________BACKGROUND_______________________________________________________________

addressformatter.py is a text parsing program written in Python 3 to ensure that
a list of email addresses conform to the formatting requirements of a 
hypothetical company: "Insurocorp".

Insurocorp has extremely strict email address formatting requirements, and
requires specific error messages for incorrectly formatted entries.

________ADDRESS_FORMATTING_______________________________________________________

Valid email addresses should be converted to lowercase, and have the following 
format:

1.  A mailbox name
2.  An “@” symbol
3.  A domain name
4.  A dot (“.”)
5.  A domain extension

The mailbox and domain names must be alphanumeric, but may have multiple parts
separated by single dots (“.”). Parts of the mailbox name may be similarly 
separated by single hyphens (“-”) and/or underscores (“_”).As an additional 
security measure, some addresses have replaced the @ symbol with “_at_” and the 
dot (before the extension) with “_dot_”.  These substitutions should be corrected. 
Given  that  all InsuroCorps’s clients are companies based in  New  Zealand, 
Australia, Canada, U.S.A., or Great Britain, the domain extension must be one of 
the follow-ing:

co.nz, com.au, co.ca, com, co.us, co.uk

Alternatively, the domain may be given in numerical form, in which case it must 
be surrounded by square brackets.

I chose to write this program in Python to take advantage of the split() method,
slice notation, dictionaries, the list class and associated methods, and the
simple indexing.

________HOW TO EXECUTE_________________________________________________________

addressformatter.py will read input from the terminal, or from a file used as an 
argument in execution. To manually input dates via terminal, navigate to the 
folder containing emailaddress.py and use the following command: 

$ python3 addressformatter.py

Type in the address you would like analysed, then press enter/return.
To quit the program, type "quit", then press enter/return.

To input a file, place the file containing dates in the same folder as 
emailaddress.py, navigate to the folder, and input the following command, 
followed by the name of the file containing your input addresses.

$ python3 addressformatter.py [filename]

________TEST_FILE_____________________________________________________________

"testfile.txt" includes the following addresses, and can be used to check if 
the program is operating correctly using the following command:

$ python3 addressformatter.py testfile.txt

Valid:
dog@InsuroCorp.com
dog_at_research.techies_dot_co.uk
dog@[139.80.91.50]

Invalid:
dog@gmail@gmail.com <--- Too many @ symbols
doggmail.com <--- Missing "@" or "_at_"
d*og@gmail.com <--- Illegal character in mailbox name
d--og@gmail.com <--- Mailbox name cannot contain two non-alphanumeric 
		     characters in a row
.dog@gmail.com <--- First character of mailbox name must be alphanumeric
dog.@gmail.com <--- Last character of mailbox name must be alphanumeric
dog@12.45.66.12] <--- Domain contains ']' but no '['
dog@gmail.cat.nz <--- Invalid domain
dog@[12.35.12.34.12] <--- Invalid domain IP format
dog@[12.12.12.270] <--- Domain IP value out of range
dog@g_dot_gmail_dot_com <--- Domain name contains multiple '_dot_'s
dog@gmail_dot_.com <--- domain name contains '_dot_' and also terminates 
                        with '.'
dog@gmailcom <--- domain name does not terminate in '.' or '_dot_'
dog@gma\l.com <--- Illegal character in domain name
dog@.gmail.com <--- First character of domain name must be alphanumeric
dog@gmail..com <--- Last character of domain name must be alphanumeric
dog@g..mail.com <--- Domain name cannot contain multiple '.' in a row

________AUTHOR________________________________________________________________

Mickey Treadwell

