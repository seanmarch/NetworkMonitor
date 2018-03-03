import nmap
import time
import smtplib
import ConfigParser
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def find_who_is_connected():

	devices_connected = []

	nm = nmap.PortScanner()

	data = nm.scan(hosts="192.168.1.1-253", arguments="-sn")

	text = (data['scan'])
	print(text)

	for key in text:
		devices_connected.append((text[key]['hostnames'][0]['name'])[:-5])

	return devices_connected


def poll_who_is_connected(previous_devices_connected):

	smtpUser = 'user@gmail.com'
	smtpPass = 'password'

	toAdd = 'user@gmail.com'
	fromAdd = smtpUser

	subject = ''
	header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject 


	nm = nmap.PortScanner()

	while True:

		current_devices_connected = []

		data = nm.scan(hosts="192.168.1.1-253", arguments="-sn")

		text = (data['scan'])

		for key in text:
			current_devices_connected.append((text[key]['hostnames'][0]['name'])[:-5])

#		new_connected_devices = set(previous_devices_connected)^set(current_devices_connected)


#		print(previous_devices_connected)
#		print(current_devices_connected)
#		print(new_connected_devices)

		new_devices_connected = set(current_devices_connected) - set(previous_devices_connected)
		devices_disconnected = set(previous_devices_connected) - set(current_devices_connected)

		message_connected = 'Connected: '
		message_disconnected = 'Disconnected: '

#		print(len(new_devices_connected))
#		print(new_devices_connected)



		if len(new_devices_connected) != 0 or len(devices_disconnected) != 0:

			for i in new_devices_connected:
				message_connected = message_connected + ' ' + str(i)
			for i in devices_disconnected:
				message_disconnected = message_disconnected + ' ' + str(i)

			body = message_connected + '  ' +  message_disconnected
			print(body)

#			print header + '\n' + body

			s = smtplib.SMTP('smtp.gmail.com',587)

			s.ehlo()
			s.starttls()
			s.ehlo()

			s.login(smtpUser, smtpPass)
			s.sendmail(fromAdd, toAdd, header + body)
			s.quit()

#			print('Devices Connected: ')
#			print('\n')
#			for i in new_devices_connected:
#				print(i)
#			print('\n')

#		print(len(devices_disconnected))
#		print(devices_disconnected)

#		if len(devices_disconnected) != 0:
#			print('Devices Disconnected: ')
#			print('\n')
#			for i in devices_disconnected:
#				print(i)
#			print('\n')

		previous_devices_connected = current_devices_connected


devices_connected = find_who_is_connected()
#print(devices_connected)
poll_who_is_connected(devices_connected)
#print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
