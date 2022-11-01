import serial
from time import sleep
import datetime
import csv
def main():
	with serial.Serial("/dev/ttyACM0",9600,timeout=1) as arduino:	
		sleep(0.1)
		if arduino.isOpen():
			print("{} connected!".format(arduino.port))
			with open("temp.csv","a") as file:
				while True:
					now = datetime.datetime.now()
					x=arduino.readline()
					y=x.rstrip("\n")
					z=y.rstrip("\r")
					if(len(y)>0):
						print(now.strftime("%Y-%m-%d %H:%M:%S"),z)
						writer = csv.writer(file)
						writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"),z])
if __name__=="__main__":
	main()
