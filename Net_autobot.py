#!/usr/local/bin/python3

import MySQLdb
import netmiko
import paramiko
import socket
import time
import datetime
import json
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
###   Warning Ignore for warnings.filterwarnings("ignore", message="CryptographyDeprecationWarning") ###
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

### Warning Ignore End ###
# export NET_TEXTFSM=/root/ntc-templates-master/templates/

def discover_cdp_nei():
	print('='*79)
	print("discovering")
	print('='*79)
#	print(connection.send_command("show cdp nei detail"))
#	print(connection.send_command('show ip int brief',use_textfsm=True))
#	print(connection.send_command('show cdp neighbors detail',use_textfsm=True))
	devices=connection.send_command('show cdp neighbors detail',use_textfsm=True)
	for device in devices:
#		print("select hostname,con_ip,location from Netdev where make='CISCO' and (hostname like %"+device['destination_host']+"% or con_ip ="+device['management_ip']+") and (type='Switch' or type='Router' or type='')" )
#		cursor.execute("select hostname,con_ip,location from Netdev where make='CISCO' and hostname like (%device['destination_host']% or con_ip =device['management_ip']) and (type='Switch' or type='Router' or type='')")
		print(device['destination_host'])
		print(device['management_ip'])
		print('+'*79)

#useful for diagram
#https://github.com/MJL85/natlas


## BEFORE USE PLZ CHANGE ##

host="localhost"
database="DATABASE"
user="USER"
password = "PASSWORD"


mydb = MySQLdb.connect(host,database,user,password)
cursor = mydb.cursor()

#cursor.execute("select con_ip, hostname from Netdev")

#cursor.execute("select hostname,con_ip,location,username,password,enable from Netdev where make='CISCO' and location='IDC_DEL' and (type='Switch' or type='Router' or type='') limit 5,17")
cursor.execute("select hostname,con_ip,location,username,password,enable from Netdev where make='CISCO' and location='IDC_DEL' and (type='Switch' or type='Router' or type='')")
#  netmiko.ssh_exception.NetMikoTimeoutException: Connection to device timed-out: cisco_ios 107.110.171.6:22
# paramiko.ssh_exception.SSHException: Incompatible version (1.5 instead of 2.0)

result = cursor.fetchall()

for i in result:
	print('~'*79)
	print(i[0])

	try:
		connection =netmiko.ConnectHandler(ip=i[1],device_type="cisco_ios",username=i[3],password=i[4],secret=i[5],timeout=5)
	except netmiko.ssh_exception.NetMikoTimeoutException:
		print('timeout')
		continue
	except paramiko.ssh_exception.SSHException:
		print('ssh version')
		continue

	connection.enable()
#	TNOW = datetime.datetime.now().replace(microsecond=0)
	TNOW = datetime.date.today()
	print(connection.send_command("show clock"))
#	print(connection.send_command('show ip int brief',use_textfsm=True))
#	print(connection.send_command("show cdp nei"))
	discover_cdp_nei()


####  SAVE FILE ####

	output = connection.send_command("show run")

	SAVE_FILE = open(i[0]+'_'+i[1]+'_'+str(TNOW)+'.txt', 'w')
	SAVE_FILE.write(output)
	SAVE_FILE.close
	print(SAVE_FILE.name)

	connection.disconnect()

