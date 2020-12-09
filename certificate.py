from PIL import ImageFont, ImageDraw, Image         # pip install pillow
import cv2                                          # pip install opencv-python
import numpy as np                                  # pip install numpy
import pandas as pd                                 # pip install pandas
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Please read the readme carefully before running any code
# https://github.com/realhunter7869/Automatic-Certificate-Generator-and-Automail

# Note that before running this file you should first run select_cood.py
# and get the co-ordinates of where exactly the receiver's name
# and certificate's name

# Initializing an instance of datetime
x = datetime.datetime.now()

# Opening the file in which data is present of receivers i.e. mail and name
# and saving them to a list
# (format : mail\tname)
# You get this kind of format when you copy and paste list of emails and names
# directly from the .csv file to .txt file (Use Excel for csv)
# Note that splitting of mail and name is not taking place in this section
f = open(input("Enter file name : "), "r")

# Opening the file where the co-ordinates are saved and extracting them
f1 = open("coords.txt", "r")
coordinates = f1.read().split("\n")

cname = input("Enter the column name where Name of the Candidate is mentioned : ")
cemail = input("Enter the column name where Email of the Candidate is mentioned : ")

print()
ds = pd.read_csv(f, usecols=[cemail, cname]) # create dataframe
print(ds)

print()
for user in ds.index:
    print(ds[cemail][user], ds[cname][user])

print()

# Taking the email and password of the sender email
# Note you have to TURN ON "Less Secure App Access" on the Google account
# It is in the Security Section of "Manage your Google Account" area
fromaddr = input("Enter sender's email : ") or "musicalnimish@gmail.com"
frompass = input("Enter sender's password : ") or "ABCD@abcd"

# Using Datetime library to get the current date and displaying it in a
# systematic way to the user
date_to_print = input("Enter date (Press Enter if current date is required) : ") or \
                (x.strftime("%d") + "/" + x.strftime("%m") + "/" + x.strftime("%Y"))

flag = True

for user in ds.index:

    toaddr = ds[cemail][user]

    name_to_print = ds[cname][user]

    # Load image in OpenCV
    image = cv2.imread("Certi2.jpg")

    # Convert the image to RGB (OpenCV uses BGR)
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Pass the image to PIL
    pil_im = Image.fromarray(cv2_im_rgb)

    draw = ImageDraw.Draw(pil_im)
    # use a truetype font
    font = ImageFont.truetype("./fonts/MLSJN.TTF", 35)      # You can change fonts from list given bottom
    font1 = ImageFont.truetype("./fonts/OLDENGL.TTF", 25)

    # Draw the text
    draw.text((int(coordinates[0]), int(coordinates[1])), name_to_print, font=font, fill='black')
    draw.text((int(coordinates[2]), int(coordinates[3])), date_to_print, font=font1, fill='blue')

    # Get back the image to OpenCV
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    if flag:
        cv2.imshow('Certificate', cv2_im_processed)       # Shows sample image
        flag = False

    path = ''
    cv2.imwrite('./output/'+name_to_print+'.png',cv2_im_processed)
    #os.startfile('output.png')
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Certificate"

    # string to store the body of the mail
    body = "Thank you for attending! \n\nHere is your certificate."

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = ds[cname][user] + ".png"
    attachment = open("output\\" + filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, frompass)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    print()
    print(f"Email sent to {ds[cname][user]}")
