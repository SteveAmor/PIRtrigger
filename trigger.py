from creds import TO_EMAIL, FROM_EMAIL, EMAIL_PASS
from gpiozero import Button, LED
from time import sleep
import datetime
import smtplib
from email.mime.text import MIMEText

lastTriggerDate = "01/01/1970"

pir = Button(21)  # Physical pin 40 (ground it to trigger)
led = LED(16)     # Physical pin 36

def sendEmail():
	# Define SMTP email server details
	smtp_server = 'smtp.gmail.com:587'
	smtp_user = FROM_EMAIL
	smtp_pass = EMAIL_PASS
	addr_from = smtp_user
	addr_to = TO_EMAIL
	subject = "First PIR trigger of the day"

	text = datetime.datetime.now().strftime('%H:%M:%S GMT %d/%m/%Y')
	msg = MIMEText(text)

	msg['To'] = addr_to
	msg['From'] = addr_from
	msg['Subject'] = subject

	try:
		# Send the message via an SMTP server
		s = smtplib.SMTP(smtp_server)
		s.starttls()
		s.login(smtp_user,smtp_pass)
		s.sendmail(addr_from, addr_to, msg.as_string())
		s.quit()
		print("%s - Email Sent OK" %subject)

	except smtplib.SMTPException:
		print("%s - Email Send Fail" %subject)

while True:
	print("Ready...")
	led.on()

	pir.wait_for_press()

	led.off()
	print("PIR triggered")

	triggerDate = datetime.datetime.now().strftime('%d/%m/%Y')

	if triggerDate != lastTriggerDate:
		sendEmail()
		lastTriggerDate = triggerDate
		print("Waiting 60 seconds.")
	else:
		print("Not the first trigger of the day.  No email sent.  Waiting 60 seconds.")

	led.blink()
	sleep(60)

