import serial

ser=serial.Serial("/dev/ttyUSB0",115200)
if ser.isOpen():
	print(ser.name+'is open...')

ser.write(b'@0gw\r')#for serial mode

