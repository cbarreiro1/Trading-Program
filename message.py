import smtplib

def send_text(message:str):
    # Email information
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SENDER_EMAIL = 'cjbarreiro1@gmail.com'
    SENDER_APP_PASSWORD = 'pctgkwjbspuclvuh'  # Replace with the generated app password

    # Recipient's phone number and SMS gateway domain (Verizon)
    RECIPIENT_NUMBER = '7574022986'
    SMS_GATEWAY_DOMAIN = 'vtext.com'

    # Compose the email address for the Verizon SMS gateway
    recipient_email = RECIPIENT_NUMBER + '@' + SMS_GATEWAY_DOMAIN

    # Create the SMTP connection
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)  # Use the app password instead of your account password

    # Send the email
    server.sendmail(SENDER_EMAIL, recipient_email, message)

    # Close the SMTP connection
    server.quit()
