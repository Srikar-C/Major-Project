import pandas as pd
import smtplib
import requests
import cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
def main(FrameNumber):
  path='OutPut/Finalnew/Bike/bike-'+str(FrameNumber)+'.jpg'
  imagepath='OutPut/Finalnew/Full/full-'+str(FrameNumber)+'.jpg'
  regions = ["in"]
  with open(path, 'rb') as fp:
   response = requests.post(
   'https://api.platerecognizer.com/v1/plate-reader/',
   data=dict(regions=regions),
   files=dict(upload=fp),
   headers={'Authorization': 'Token a64960c78ce3493a81dae7422b011f3a66a342a2'})
   res = response.json()
   print(res)
   if (len(res['results']) > 0):
        num_plt = res['results'][0]['plate'].upper()
        input_number_plate = num_plt
        excel_file_path = r'C:\Users\GANGADHAR\Desktop/exampleExcel.xlsx'
        df = pd.read_excel(excel_file_path)
        if input_number_plate in df['Number Plate'].values:
            print("Number plate found!")
            print(f"Number Plate is {num_plt}")
            email_id = df[df['Number Plate'] == input_number_plate]['Email ID'].values[0]
            print(f"Email ID: {email_id}")
            email_sender = "agangu0629@gmail.com"
            email_password = "jale qukn zsdb iusl"
            email_receiver = email_id
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_sender, email_password)
            message = MIMEMultipart()
            message['From'] = email_sender
            message['To'] = email_receiver
            message['Subject'] = "Fine by violating the rules"
            message.attach(MIMEText("You are caught by using helmet and triple riding\nPay fine 140 Rupees.", 'plain'))
            with open(imagepath, "rb") as image_file:
                image = MIMEImage(image_file.read(), _subtype="jpg")
            image.add_header('Content-Disposition', 'attachment', filename="your_image.jpg")
            message.attach(image)
            email_text = message.as_string()
            server.sendmail(email_sender, email_receiver, email_text)
            server.quit()
            print("Email Sent with Attachment")
        else:
            print(f"Number Plate is {num_plt}")
            print("Number plate not found in the Excel sheet.")
   else:
    num_plt = "not recognized"
    print('Number plate not Recognized')
    exit

if __name__=='__main__':
  main(5)