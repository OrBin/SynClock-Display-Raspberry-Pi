from datetime import datetime
import requests
import time
import sys
from Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack import LEDBackpack
import logging

segment = SevenSegment(address=0x70)
led_disp = segment.disp
CONFIG_FILE_NAME = ".raspi_clock_display_config"

conf_file = open(CONFIG_FILE_NAME, "r")
get_time_path = conf_file.read().strip()
conf_file.close()

logging.basicConfig(filename='log.txt',level=logging.INFO, format="%(asctime)s %(levelname)s %(module)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S %Z')

logging.info('Path to get time from: "%s"' % get_time_path)

while True:
	try:
		print datetime.now()
		r = requests.get(get_time_path, timeout=5)

		if r.status_code != 200:
			raise Exception("Could not connect to get the time")

		alarm_datetime = datetime.fromtimestamp(int(str(r.text).split()[0]))
		difference_in_days = ((alarm_datetime - datetime.now()).total_seconds()/60/60/24)
		led_disp.setBlinkRate(0)
        
		if difference_in_days < 1 and difference_in_days > 0:
			segment.writeDigit(0, alarm_datetime.hour / 10)   
			segment.writeDigit(1, alarm_datetime.hour % 10)   
			segment.writeDigit(3, alarm_datetime.minute / 10)   
			segment.writeDigit(4, alarm_datetime.minute % 10)   
			segment.setColon(SevenSegment.ColonParts.RIGHT_COLON, True)
			logging.info('Next alarm: %s', alarm_datetime)
		else:
			for digit in [0, 1, 3, 4]:
				segment.writeDigitRaw(digit, 0b1000000)
			segment.setColon(SevenSegment.ColonParts.RIGHT_COLON, False)
			logging.info('No alarm for the next 24 hours')
	except Exception, e:
                logging.exception(e)
		# Blink 7Segment
		led_disp.setBlinkRate(2)
		logging.error('Error, blinking')
	time.sleep(5)
