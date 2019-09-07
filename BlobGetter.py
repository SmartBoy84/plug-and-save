import os
import platform
import subprocess
import sys
import time
import urllib.request as urllib2
import json
import pprint

def list_signed(device):
	url = "https://api.ipsw.me/v4/device/" + device
	json_file = urllib2.urlopen(url)
	with open("signed.json",'wb') as output:
		output.write(json_file.read())

	data = json.load(open("signed.json"))
	i = 0
	with open("signed.json"):
		print("signed firmwares for %s:" % device)
		for i in range(0, len(data["firmwares"])):
			if data["firmwares"][i]["signed"] == True :
				print("%s - %s" % (data["firmwares"][i]["version"], data["firmwares"][i]["buildid"]))
			i+=1
	os.remove("signed.json")

def cls():
    os.system('cls')

output = ""
first = ""
second = ""
rec = ""

udid = ""
ecid = ""
nonce = ""
model = ""

ios = ""
cls()
print("A12 Plug-And-Save!")
print("\n*Make sure you have iTunes installed!")

print("\n*Make sure you have a definate generator")
print("Check out the nonce.txt file to see how")

print("\nPress enter when ready to proceed")
input()
cls()
print("Plug in your device, trust your computer and setup via iTunes")
print("Press enter when device has properly connected (Can iTunes see it?)")
input()
cls()
print("***Entering recovery mode***")
print("\nFinding UDID...")
output = str(subprocess.check_output("ideviceinfo.exe", shell=True))
first = int(output.find("UniqueDeviceID")+16)
second = int(output.find("UseRaptorCerts")-4)
udid = output[first:second]
first = int(output.find("ProductType")+13)
second = int(output.find("ProductVersion")-4)
model = output[first:second]
print("UDID: "+udid)
print("Model: "+model)
os.system("ideviceenterrecovery.exe "+udid)
time.sleep(8)
print("\nEntered!")
time.sleep(1)
cls()
print("***Finding the nonce and ECID***\n")
rec = str(subprocess.check_output("irecovery.exe -q", shell=True))
first = int(rec.find("ECID")+6)
second = int(rec.find("CPFM")-4)
ecid = rec[first:second]
print("ECID: "+ecid)
first = int(rec.find("NONC")+6)
second = int(rec.find("SNON")-4)
nonce = rec[first:second]
print("ApNonce: "+nonce)
print("Exiting recovery mode...")
os.system("irecovery.exe -n")
cls()
print("***Geting blobs****")
print("Feel free to disconnect your device!")
print("\nInfo:")
print("UDID: "+udid)
print("ECID: "+ecid)
print("ApNonce: "+nonce)
print("Model: "+model)
print("\nWhat iOS version's blob do you want?")
print("Make sure it is currently signed!")
list_signed(model)
print("\nType L for latest")
ios = input("Version (E.g. 12.4): ")
if ios == "l" or ios == "L":
    print("\nGetin' the latest blobs baby!")
    os.system("tsschecker.exe -e "+ecid+" -l --apnonce "+nonce+" -d "+model+" -s")
else:
    print("\nGeting the blobs for iOS "+ios)
    os.system("tsschecker.exe -e "+ecid+" -i "+ ios +" --apnonce "+nonce+" -d "+model+" -s")
print("\nDone and dusted!")
print("BTW I saved your device info in info.txt")
input()

