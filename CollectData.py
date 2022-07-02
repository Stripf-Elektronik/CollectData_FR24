#git@github.com:Stripf-Elektronik/CollectData_FR24.git

import os
import socket
from datetime import datetime

HOST = "192.168.178.60" #IP-Adresse des Pi
PORT = 30003 #Port ist immer 30003

Str_Temperatur = str("")
Str_Spannung = str("")
Str_Uptime = str("")
Str_Now = str("")

if os.path.isfile("FR24Status.txt"):
    os.remove("FR24Status.txt")

#Daten Sammeln und schreiben:
Str_Temperatur = os.popen("vcgencmd measure_temp").readline()
Str_Spannung = os.popen("vcgencmd measure_volts").readline()
Str_Uptime = os.popen("uptime").readline()
now = datetime.now()
Str_Now = now.strftime("Datum: "+"%d.%m.%y" + " Uhrzeit:" + "%H:%M:%S")
    
file = open("FR24Status.txt","w")
file.write("Gesammelte Daten zu ADS-B Groundstation T-EDSB186:" + "\n" + "\n")
file.write("Zeitstempel: " + Str_Now + "\n" + "\n")
file.write("CPU-Temperatur: " + Str_Temperatur + "\n")
file.write("CPU-Spannung: " + Str_Spannung + "\n")
file.write("Zeit seit Neustart: " + Str_Uptime + "\n" + "\n" + "\n")
file.write("Statusabfrage des FR24-Feeder:" + "\n")
file.close()

os.popen("fr24feed-status >> FR24Status.txt")

file = open("FR24Status.txt","a")
file.write("\n" + "\n")
file.write("Die letzten 10 empfangenen Buffer von Port 3003:" + "\n")
file.close()

for i in range(11):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    data = 0
    data = s.recv(16384)
    file = open("FR24Status.txt","a")
    file.write("Buffer " + str(i) +": " + data)
    file.close()

file = open("FR24Status.txt","a")
file.write("\n" + "\n")
file.write("Uebersicht IP-Adresse und Netzwerkeinstellungen:" + "\n")
file.close()
# Uebersicht der IP-Einstellungen in Datei schreiben
os.popen("ip a >> FR24Status.txt")

#Daten per Mail versenden
os.system ("python SendStatusmail.py FR24Status.txt") 
