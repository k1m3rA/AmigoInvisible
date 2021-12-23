import random
# Import smtp module
import smtplib
import config

# Create a function that ask for the user for names and their emails
def ask_for_names_and_emails():
    # Clear the screen
    print("\033c")
    # Ask for the user for names and their emails
    names_and_emails = {}
    # Ask for the user for the number of names and emails
    num_names_and_emails = int(input("¿Cuántos nombres y correos desea introducir? "))
    # Ask for the user for the names and emails and check if the input is a valid email. If it is not valid retry until it is valid.
    
    for i in range(num_names_and_emails):
        # Ask for the user for the name
        name = input("Write the " + str(i+1) + "º name: ")
        # Ask for the user for the email
        email = input("Write the email of " + name + ": ")
        # While it is not a valid email, retry until it is valid
        while "@" not in email and "." not in email:
            print("The email of " + name + " is not valid, try again.")
            email = input("Write the email of " + name + ": ")
        # Add the name and email to the dictionary
        names_and_emails[name] = email
    # Return the dictionary
    return names_and_emails


# Create a function that sends an email with the given parameters
def send_email(remitente, clave, host, port, destinatario, asunto, mensaje):
    # Create a SMTP object
    s = smtplib.SMTP(host, port)
    # Start TLS encryption
    s.starttls()
    # Login with the given credentials
    s.login(remitente, clave)
    # Send the email
    s.sendmail(remitente, destinatario, "Subject: {}\n\n{}".format(asunto, mensaje))
    # Close the connection
    s.quit()



# Create a dictionary defining random doubles with a given list without repeating items
def create_random_doubles(list_names):
    random_doubles = {}
    # Shuffle list
    random.shuffle(list_names)
    for i in range(len(list_names)):
        # Defines the i element of list_names as the key and the next element as the value, if the key is the last element, the value is the first element.
        random_doubles[list_names[i]] = list_names[i+1] if i+1 < len(list_names) else list_names[0]

    return random_doubles

# Main function that calls the create_random_doubles function and pass the list of doubles.
if __name__ == "__main__":
    # Create a dictionary with the names and emails
    names_and_emails = ask_for_names_and_emails()
    # Create a list of names out of the dictionary created in the ask_for_names_and_emails function
    names = list(names_and_emails.keys())
    # Checks if the list is empty
    if len(names) > 0:
        random_doubles = create_random_doubles(names)
        # Send an email to each key in random_doubles with a string with the value of the key as message
        for key in random_doubles:
            # Send an email to the key with the value of the key as message. Also check if theres an error and if there is, exit the program with message.
            try:
                send_email(config.remitente, config.clave, config.host, config.port, names_and_emails[key], "Amigo Invisible", "Tu amigo invisible es " + random_doubles[key])
                # Show in screen a message that the email was sent successfully
                print(key + " has recieved the invisible friend.")
            except smtplib.SMTPRecipientsRefused:
                print("There was an error sending the email to " + key + ".")
                exit()
    # Exit if the list is empty
    else:
        print("The list was empty")
        exit()
