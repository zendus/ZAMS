import csv
import smtplib
import datetime
import numpy as np
from runapp import app
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from sqldb import db, Student_details

    

#create spreadsheet
def create_spreadsheet(predicted_names, course_handler_email, lect):
    Id = 0
    print(predicted_names)
    current_date_and_time = datetime.datetime.now(tz=None).strftime("%d/%m/%Y, %H:%M" )
    current_seconds = datetime.datetime.now(tz=None).strftime("%S")
    file_name = "Attendance_sheet%s.csv" % (current_seconds)
    # csv_file_path = r".\spreadsheets\Attendance_sheet%s.csv" % (current_seconds)
    csv_file_path = "./spreadsheets/" + file_name
    while Id < len(predicted_names):
        with open(csv_file_path, 'a+', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            #fetch details from the sql db and add to row
            details = Student_details.query.filter_by(firstname=predicted_names[Id])
            regnum = str(details.all()[0]).split(',')[0]
            firstName = str(details.all()[0]).split(',')[1]
            lastName = str(details.all()[0]).split(',')[2]
            level = str(details.all()[0]).split(',')[3]
            dept = str(details.all()[0]).split(',')[4]
            heading = ['Registration Number', 'Firstname', 'Lastname', 'Level', 'Department', 'Course']
            #added ESUT/ to counter excel displaying regnum with scientific notation
            row = ['ESUT/' + regnum, firstName, lastName, level, dept, lect]
            date_row = ['CREATED', current_date_and_time]
            if Id == 0:
                writer.writerow(date_row)
                writer.writerow(heading)
                writer.writerow(row)
            else:
                writer.writerow(row)
        csv_file.close()
        Id += 1
    print(str(file_name) + ' created successfully')
    send_email(course_handler_email, file_name)


#send spreadsheet to email
def send_email(course_handler_email, file_name):
    mail_content = 'Here is your attendance management file for today'
    password = app.config['PASSWORD']
    gmail_tcp_port = 587
    origin_email = app.config['EMAIL']
    
    #set up MIME
    message = MIMEMultipart('mixed')
    message['From'] = origin_email
    message['To'] = course_handler_email
    message['Subject'] = 'ZENDUS Attendance Management System'

    #attach text
    alternative = MIMEMultipart('alternative')
    mail_text_content = "Here is the attendance file for today's lecture"
    textplain = MIMEText (mail_content)
    alternative.attach(textplain)
    message.attach(alternative)

    #attach file
    filename = file_name
    path = "./spreadsheets/"
    full_path = path + filename
    xlsxpart = MIMEApplication(open(full_path, 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(xlsxpart)
    try:
        server = smtplib.SMTP("smtp.gmail.com", gmail_tcp_port)
        server.starttls() #turn on encryption between user and gmail
        server.login(origin_email, password)
        item = message.as_string()
        server.sendmail(origin_email, course_handler_email, item)
        server.quit()
        print('email successfully sent !!!')
    except smtplib.SMTPRecipientsRefused:
        print('Email delivery failed, invalid recipient')
    except smtplib.SMTPAuthenticationError:
        print('Email delivery failed, authorization error')
    except smtplib.SMTPSenderRefused:
        print('Email delivery failed, invalid sender') 


