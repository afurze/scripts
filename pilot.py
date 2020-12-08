import board
import busio
import digitalio
import adafruit_max31856
import logging
import os
import requests
from tendo import singleton
import time


# Sends the pilot light out email
def send_mail():
	api_secret = os.environ['MAILGUN_API_PRIVATE']
	logging.info('Sending email alert')
	logging.debug('API secret: %s', api_secret)

	response = requests.post(
		'https://api.mailgun.net/v3/sandboxd8f8a4c9c2e649288d536b191458544c.mailgun.org/messages',
		auth=('api', api_secret),
		data={
			'from': 'furze.andrew@gmail.com',
			'to': ['furze.andrew@gmail.com'],
			'subject': 'Pilot Out',
			'text': 'Pilot out'
		}
	)

	logging.debug(response)


def main():
	# Singleton housekeeping
	me = singleton.SingleInstance()

	# Setup logging
	root_logger = logging.getLogger()
	root_logger.setLevel(logging.INFO)
	handler = logging.FileHandler('pilot.log', 'a', 'utf-8')
	handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
	root_logger.addHandler(handler)

	# Open thermocouple for reading
	spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
	cs = digitalio.DigitalInOut(board.D5)
	cs.direction = digitalio.Direction.OUTPUT
	max31856 = adafruit_max31856.MAX31856(spi, cs)

	while(True):
		currentTemp = max31856.temperature
		logging.info('Current temp: %s', currentTemp)
		if (currentTemp < 35):
			send_mail()
		time.sleep(60)


if __name__ == '__main__':
	main()
