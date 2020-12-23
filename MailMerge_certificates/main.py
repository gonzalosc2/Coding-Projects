# author: Gonzalo Salazar
# name: certificates generation and its sending process
# description: This code generates a set of certificates from a list of participants,
#              in a congress (or any activity), which are then converted to pdf and 
#              sent individually via email (with a personalized message), to each 
#              participant.

#%%
### LIBRARIES ###
import os
import pandas as pd
from mailmerge import MailMerge
from docx2pdf import convert
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from getpass import getpass

### SETTING WD ###
wdpath = '/Users/gsalazar/Documents/C_Codes/Coding-Projects/MailMerge_certificates'
os.chdir(wdpath)

#%%
### FUNCTIONS DEFINITION ###

def file_checking():
    "Checks whether a files exists or not. Quits the program if required by the user."
    "   INPUT: N/A"
    "   OUTPUT: a string with a file name (if does not exist) or nothing "
    "           (if the user decides to quit)   "

    while True:
        try:
            filename = input('Type here: ')
            
            if filename.upper() == 'QUIT':
                quit()
            
            with open(filename, 'r'):
                return filename

        except IOError:
            print('\nSorry, but the file named ' + filename + \
                  'does not exist. Please provide the correct name.\n')
            continue

def file_prompting():
    "Asks for the name and extension of the files required to generate the certificates."
    "   INPUT: N/A"
    "   OUTPUT: a list (with filenames)"
    
    print('\nProvide the name of the template file. Include its extension as well. ' + 
            'If you want to exit type QUIT: ')
    template_f = file_checking()

    print('\nProvide the name of the file containing the list of participants. ' +
                        'Include its extension as well. If you want to exit type QUIT: ')
    participants_f = file_checking()

    return [template_f,participants_f]    

def folder_creation():
    "Creates directories where all generated certificates will be saved"
    "   INPUT: N/A"
    "   OUTPUT: two new folders (if they did not exist previously) and a message acknowledging"
    "           their creation (they will show up even if folders were already there; mainly used"
    "           to know that the previous command worked well)"
    
    parent_dir = os.getcwd()
    os.makedirs(os.path.join(parent_dir,'dp_Word'), exist_ok = True)  # creates a directory for .docx files
    print('Directory {} has been created'.format('dp_Word'))          
    os.makedirs(os.path.join(parent_dir,'dp_PDF'), exist_ok = True)   # creates a directory for .pdf files
    print('Directory {} has been created'.format('dp_PDF'))           

def merging_process():
    "Merges a list of participants with a template file (a certificate)"
    "   INPUT: N/A"
    "   OUTPUT: a set of files in .docx format (personalized certificates)"
    
    global list_f
    temp_f = files[0]
    list_f = files[1]

    global df
    df = pd.read_csv(list_f)
    df['Additional Last Name'].fillna(value = '', inplace = True)  # essential, otherwise it will drop names
    df['Full_Name'] = df['Names'].str.title().str.strip() + ' ' + \
                            df['Last Name'].str.title().str.strip() + ' ' + \
                            df['Additional Last Name'].str.title().str.strip()
    df['Full_Name'].apply(str.strip)                        
    df.sort_values(by = 'Full_Name', inplace = True)                        
    for index, row in df.iterrows():
        with MailMerge(temp_f) as f:
            f.merge(Full_Name = str(row['Full_Name']))
            name = str(row['Full_Name'])
            f.write(f'./dp_Word/diploma_{name}.docx')

def docx_to_pdf():
    "Converts from .docx format to .pdf format each file (certificate)"
    "   INPUT: N/A"
    "   OUTPUT: a set of files in .pdf format (personalized certificates)"
    
    convert('dp_Word/','dp_PDF/')

def email_config(body,sender_email,sender_pass,receiver_email,filename):   
    "Creates parts of a personalized email (body, subject, sender and receiver)"
    "   INPUT: a bunch of strings (body, sender's email, sender's password,"
    "          receiver's email and a filename to be attached)"
    "   OUTPUT: an exception if an email cannot be sent"

    msg = MIMEMultipart()
    msg['Subject'] = 'Certificate of Participation - First Home-Coding Congress'           # can be modified
    msg['From'] = 'Organizing Committee - First Home-Coding Congress'                      # can be modified
    msg['To'] = receiver_email                                                             # can be modified
    
    msgText = MIMEText(body, 'plain')
    msg.attach(msgText)

    filepath = './dp_PDF/diploma_' + filename + '.pdf'
    pdf = MIMEApplication(open(filepath,'rb').read())
    pdf.add_header('Content-Disposition','attachment',filename = 'Diploma - ' + filename + '.pdf')
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.gmail.com',587) as smtp_object:
            smtp_object.ehlo()  # tells us the state of our connection
            smtp_object.starttls()
            smtp_object.login(sender_email,sender_pass)
            smtp_object.sendmail(sender_email,receiver_email,msg.as_string())
    except Exception as e:
        print(e)

def email_sending():
    "Sends and creates parts of a personalized email (body and receiver)"
    "   INPUT: N/A"
    "   OUTPUT: N/A"

    global df
                     
    sender_email = getpass("\nEnter sender's email here (if you want to exit type QUIT): ")

    if sender_email.upper() == 'QUIT':
        quit()

    sender_pass = getpass("\nEnter sender apps' pass here: ")  # app password is required for gmail server (if two-steps verification is activated)

    for index,row in df.iterrows():
        receiver_email = row['Email Address']    
        receiver_name = row['Full_Name']
        body = 'Dear ' + receiver_name + ':' +  "\n\n\nOn behalf of the Coding Learner's Institute and the founder of trustAI Consulting, " + \
                'Gonzalo S. Trusted. We thank you for attending to the First Home-Coding Congress held at home! Attached you will find ' + \
                'your certificate of participation.' + \
               '\n\nWe hope this activity had fulfilled your expectations as well as it had contributed to your professional life.' + \
               '\n\n\nSincerely,\n\nOrganizing Committee\nFirst Home-Coding Congress'      # can be modified
        email_config(body,sender_email,sender_pass,receiver_email,receiver_name)

#%%
def main():
    "Runs the whole code"
    "   INPUT: N/A"
    "   OUTPUT: string prompting for files (.docx and .pdf), an email address and its password (both for the sender)"
    
    global files
    global list_f
    global df

    # dwdw
    files = file_prompting()

    # dwdw
    folder_creation()

    # dwdw
    merging_process()

    # dwdw
    docx_to_pdf()

    # dwdw
    email_sending()

main()