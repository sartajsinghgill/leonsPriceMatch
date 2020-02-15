from lxml import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import smtplib, ssl
import requests
import re

#This function will find the price of the item from the URL that is passed to it. Used a regex to find the exact item in the HTML.
def findPriceOfItem(url):
    r = requests.get(url)
    htmlPage = html.fromstring(r.content)
    prices = re.sub("$|,", "", htmlPage.xpath('//span[@id="productPrice"]/text()')[0]).strip('$')
    return prices

#Get the prices for the items from the leons website and store to a variable to compare.
sevenPiecePrice = float(findPriceOfItem('https://leons.ca/products/cleopatra-7-piece-dining-room-set-oak'))
ninePiecePrice = float(findPriceOfItem('https://leons.ca/products/cleopatra-9-piece-dining-room-set-oak'))
serverPrice = float(findPriceOfItem('https://leons.ca/products/cleopatra-server-oak'))
sofaPrice = float(findPriceOfItem('https://leons.ca/products/stampede-sofa-brown'))
diningChairPrice = float(findPriceOfItem('https://leons.ca/products/cleopatra-side-chair-light-brown'))
accentChairPrice = float(findPriceOfItem('https://leons.ca/products/rowena-accent-chair-white-and-grey'))

#Prices for the items when purchased.
sevenPiecePurchasePrice = 1928
ninePiecePurchasePrice = 2274
serverPurchasePrice = 899
sofaPurchasePrice = 1599
diningChairPurchasePrice = 183
accentChairPurchasePrice = 399

sevenPieceMessage = ""
ninePieceMessage = ""
serverMessage = ""
sofaMessage = ""
diningChairMessage = ""
accentChairMessage = ""

#This is the flag that triggers whether an email needs to be sent or not.
sendEmail = False

#Check 7 piece dining set price
if sevenPiecePrice < sevenPiecePurchasePrice:
    sevenPieceMessage = "<h3>7 piece cheaper now - Purchased for: "+str(sevenPiecePurchasePrice)+" , Now price: "+str(sevenPiecePrice)+"</h3>"
    sendEmail = True
else:
    sevenPieceMessage = "You bought the 7 piece for cheaper"

#Check 9 piece dining set price
if ninePiecePrice < ninePiecePurchasePrice:
    ninePieceMessage = "<h3>9 piece cheaper now - Purchased for: "+str(ninePiecePurchasePrice)+" , Now price: "+str(ninePiecePrice)+"</h3>"
    sendEmail = True
else:
    ninePieceMessage = "You bought the 9 piece for cheaper"

#Check server price
if serverPrice < serverPurchasePrice:
    serverMessage = "<h3>Server cheaper now - Purchased for: "+str(serverPurchasePrice)+" , Now price: "+str(serverPrice)+"</h3>"
    sendEmail = True
else:
    serverMessage = "You bought the server for cheaper"

#Check sofa price
if sofaPrice < sofaPurchasePrice:
    sofaMessage = "<h3>Sofa cheaper now - Purchased for: "+str(sofaPurchasePrice)+" , Now price: "+str(sofaPrice)+"</h3>"
    sendEmail = True
else:
    sofaMessage = "You bought the sofa for cheaper"

#Check dining chair price
if diningChairPrice < diningChairPurchasePrice:
    diningChairMessage = "<h3>Dining chair cheaper now - Purchased for: "+str(diningChairPurchasePrice)+" , Now price: "+str(diningChairPrice)+"</h3>"
    sendEmail = True
else:
    diningChairMessage = "You bought the dining chair for cheaper"

#Check accent chair price
if accentChairPrice < accentChairPurchasePrice:
    accentChairMessage = "<h3>Accent chair cheaper now - Purchased for: "+str(accentChairPurchasePrice)+" , Now price: "+str(accentChairPrice)+"</h3>"
    sendEmail = True
else:
    accentChairMessage = "You bought the accent chair for cheaper"

#Opening the HTML file to update.
htmlPage = open('/var/www/html/leons.html','w')

#Message template that will form the html page with the list of all the items and shows if anything is cheaper now.
message = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Leons Price Checker</title>
</head>
<body>
    %s<br />
    %s<br />
    %s<br />
    %s<br />
    %s<br />
    %s<br />
    This is as of : %s
</body>
</html>"""

#Write to the html page with the values of all of the messages as per the conditions from above
htmlPage.write(message % (sevenPieceMessage, ninePieceMessage, serverMessage, sofaMessage, diningChairMessage, accentChairMessage, datetime.datetime.now()))

#Update the sender email, receiver email and password. The SMTP settings are for the email address that is used for sending emails. Here the sender email address is gmail.
sender_email = ""
receiver_email = ""
password = ("")

#Following code sets the required values for th eemail message and then sends the email.
emailMessage = MIMEMultipart("alternative")
emailMessage["Subject"] = "Leons Price Alert"
emailMessage["From"] = sender_email
emailMessage["To"] = receiver_email

emailMessage.attach(MIMEText(message, "html"))

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    if sendEmail:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, emailMessage.as_string() % (sevenPieceMessage, ninePieceMessage, serverMessage, sofaMessage, diningChairMessage, accentChairMessage, datetime.datetime.now())
        )