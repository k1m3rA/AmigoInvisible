import random
import smtplib
import json
import csv
import argparse
from email.message import EmailMessage

# Import contacts from text file
def import_contacts(argument):
    
    with open(argument, 'r') as file:
        try:
            # Creates a reader object to read the file
            reader = csv.reader(file, delimiter=':')
        except:
            print("Error: Invalid file format")
            exit()
        
        # Creates an empty list to save changes
        contacts = []

        # Iterates each element
        for name, email in reader:
            # Creates a dictionary with two keys: name and email
            contact = {'name': name, 'email': email}

            # Adds the dictionary to list
            contacts.append(contact)

    return contacts

# Send email function
def send_email(addressee, msg):

    # Create a SMTP object
    s = smtplib.SMTP(config["host"], config["port"])
    # Start TLS encryption
    s.starttls()
    
    # Create the message
    msg_processed = EmailMessage()
    msg_processed.set_content(msg)

    # Add custom From field
    # with remitter name and email
    msg_processed.add_header('From', config["name"] + ' <' + config["remitter"] + '>')
    msg_processed.add_header('Subject', "Invisble Friend")

    # Login with the given credentials
    s.login(config["remitter"], config["password"])
    # Send the email
    s.sendmail(config["remitter"], addressee, msg_processed.as_string())
    # Close the connection
    s.quit()

# Deliver the friends list
def deliver(contacts):
    # This is an example of contacts list imported by import_contacts()
    # contactos = [{"name" : "robin", "email": "robin@gmail.com"}, {"name": "joseph", "email": "joseph@gmail.com"}, {"name": "kimera", "email": "kimera@gmail.com"}]

    random.shuffle(contacts)

    for i in range(0, len(contacts)):
        try:
            send_email(contacts[i]["email"], "Your Invisible Friend is " + contacts[(i+1)%len(contacts)]["name"])
            # Show in screen a message that the email was sent successfully
            print(contacts[i]["name"] + " has recieved the invisible friend.")
        except smtplib.SMTPRecipientsRefused:
            print("There was an error sending the email to " + contacts[i]["name"] + ".")
            exit()

# Import configuration
with open("config.json") as f:
    config = json.load(f)
    f.close()

# Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", type=str, help="Contacts file", required=True, dest="filename")
args = parser.parse_args()

# If file arg provided launch default flow
if args.filename:
    deliver(import_contacts(args.filename))
