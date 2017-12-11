import smtplib
from email.message import EmailMessage
from firebase_admin import credentials, db
from firebase import firebase

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("omgnooopython@gmail.com", "pythonnopython")

# userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
# allUser = userFire.get('allUsers',None)
# allName= []
# for key in allUser:
#     allName.append(allUser[key]['Email'])

msg = EmailMessage()
msg['Subject'] = 'The Foodie'
msg['From'] = 'thefoodie.newsletter@gmail.com'
msg['To'] = '172862A@mymail.nyp.edu.sg'

msg.set_content("Thank you for subscribing with The Foodie Newsletter! Look forward to monthly newsletters and also exclusive discount codes for subscribers!")
server.send_message(msg)
server.quit()

