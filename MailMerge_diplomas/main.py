# author: Gonzalo Salazar
# name: diploma generation and its sending process
# description: This code generates a set of diplomas from a list of participants,
#              in a congress, which are then converted to pdf and sent individually,
#              to each participant.

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

#%%
### FUNCTIONS DEFINITION ###

def file_checking():
    " "
    "   INPUT: "
    "   OUTPUT: "

    while True:
        try:
            filename = input('Type here: ')
         
            if filename.upper() == 'QUIT':
                quit()
            else: 
                break

        except IOError:
            print('\nSorry, but there is no file named ' + filename + \
                '. Please provide the correct name.\n')
            continue

    return filename

def file_prompting():
    " "
    "   INPUT: "
    "   OUTPUT: "
    
    print('\nProvide the name of the template file. Include its extension as well. ' + 
            'If you want to exit type QUIT: ')
    template_f = file_checking()

    print('\nProvide the name of the file containing the list of participants. ' +
                        'Include its extension as well. If you want to exit type QUIT: ')
    participants_f = file_checking()

    return [template_f,participants_f]    

def merging_process(files):
    "Merges a list of participants with a template file (diploma)"
    "   INPUT: a template file and csv file with a list of participants"
    "   OUTPUT: a set of files (personalized diplomas)"

    temp_f = files[0]
    list_f = files[1]

    df = pd.read_csv(list_f)
    df['Apellido Materno'].fillna(value = '', inplace = True)  # essential, otherwise it will drop names
    df['Nombre_Completo'] = df['Nombres'].str.title().str.strip() + ' ' + \
                            df['Apellido Paterno'].str.title().str.strip() + ' ' + \
                            df['Apellido Materno'].str.title().str.strip()
    df.sort_values(by = 'Nombre_Completo', inplace = True)                        
    for index, row in df.iterrows():
        with MailMerge(temp_f) as f:
            f.merge(Nombre_Completo = str(row['Nombre_Completo']))
            name = str(row['Nombre_Completo'])
            f.write(f'./dp_Word/diploma_{name}.docx')

def docx_to_pdf():
    ""
    "   INPUT: "
    "   OUTPUT: "
    
    convert('dp_Word/','dp_PDF/')

def email_sending(body,sender_email,sender_pass,receiver_email,filename):   
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Diploma - Congreso de tragrasables en Miami'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    filename = './dp_PDF/diploma_' + filename + '.pdf'
    pdf = MIMEApplication(open(filename,'rb').read())
    pdf.add_header('Content-Disposition','attachment',filename = filename)
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.gmail.com',587) as smtp_object:
            smtp_object.ehlo()  # tells us the state of our connection
            smtp_object.starttls()
            smtp_object.login(sender_email,sender_pass)
            smtp_object.sendmail(sender_email,receiver_email,msg.as_string())
    except Exception as e:
        print(e!)

# %%
files = ['broma.docx','broma.csv']
merging_process(files)

# %%
docx_to_pdf()

# %%
# 