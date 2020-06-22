mport board
import busio
import digitalio
import adafruit_max31856
import os
from mailjet_rest import Client
import time


# Housekeeping, check if another instance is running
def singleton_check():
	try:
		with open('pilot.pid', 'r') as f:
			pid = f.readline()
			try:
				os.kill(pid, 0)
			except OSError:
				# Safe, previous pid is dead
				pass
			else:
				# Abort!
				sys.exit()
	except:
		pass

	# Update the pid file with our pid
	with open('pilot.pid', 'w') as f:
		pid = os.getpid()
		f.write(str(pid))


# Read temp from Adafruit MAX313856
def get_temp():
	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
	cs = digitalio.DigitalInOut(board.D5)
	cs.direction = digitalio.Direction.OUTPUT
	max31856 = adafruit_max31856.MAX31856(spi, cs)

	return(max31856.temperature)


# Sends the pilot light out email
def send_mail():
	api_key = os.environ['MJ_APIKEY_PUBLIC']
	api_secret = os.environ['MJ_APIKEY_PRIVATE']
	mailjet = Client(auth=(api_key, api_secret), version='v3.1')
	data = {
		'Messages': [
			{
				'From': {
					'Email': 'furze.andrew@gmail.com',
					'Name': 'Andrew Furze'
				},
				'To': [
					{
						'Email': 'furze.andrew@gmail.com',
						'Name': 'Andrew Furze'
					}
				],
				'Subject': 'Pilot light out',
				'TextPart': 'Pilot light out'
			}
		]
	}
	result = mailjet.send.create(data=data)


def main():
	singleton_check()
	# Run a temp check every 5 minutes
	while(True):
		temp = get_temp()
		if (temp < 35):
			send_mail()
	time.sleep(3600)


if __name__ == '__main__':
	main()
