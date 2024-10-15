import asyncio
import datetime
import csv
import getpass
import time
from time import sleep

import bleak  # bleak library
from bleak import BleakClient

import sys


now = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M')
print(now)


# # NRF BML DEVICE 1
# address = 'ED:06:80:63:AD:55' # this must be changed when you connect new device.
# UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
# send_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

# NRF BML DEVICE 2
address = 'D9:24:2C:68:2C:E0' # this must be changed when you connect new device.
UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
send_uuid = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

'''
# ESP 32
address = '10:52:1c:66:7e:92' # this must be changed when you connect new device.
UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
send_uuid = "beb5483e-36e1-4688-b7f5-ea07361b26a8"
'''

# it works only windows.
username = getpass.getuser()
lineCounter = 0

# set sleep time to control frequency of incoming data
sleep_time = 0.5

def writeLog(username, coordinates):
    global lineCounter
    lineCounter = lineCounter + 1
    log_path = 'C:/Users/' + username + '/Downloads/' + now + '_ABALONE.csv'
    with open(log_path, 'a', newline='') as f:
        wr = csv.writer(f)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        wr.writerow([current_time] + coordinates)
        #print([current_time] + coordinates)
        #print('Finished writing line ' + str(lineCounter) + ' to csv')

def callback(sender, data):
    l_data = data.decode().split(',')
    writeLog(username, l_data)
    print(l_data)

    # originally every 10 minutes = 600s, this is set to every 1s for the magnetometer magnitude to distance experiment
    time.sleep(sleep_time)


async def connect(address):
    print("starting", address, "loop")
    async with BleakClient(address, timeout=20.0) as client:
        print("connected to", address)
        await client.start_notify(UUID, callback)

        # originally every 20ms = 0.02, this is set to every 1s for the magnetometer magnitude to distance experiment
        await asyncio.sleep(sleep_time)

        loop = asyncio.get_running_loop()
        while True:
            # command = await loop.run_in_executor(None, input, "Enter 'disconnect' to disconnect, 'stop' to stop measuering, 'resume' to resume measuering : \r\n")
            command = await loop.run_in_executor(None, input, "Enter 'stop' to stop measuering, 'resume' to resume measuering : \r\n")
            print(command.strip().lower())
            if command.strip().lower() == 'stop':
                await client.write_gatt_char(send_uuid, 'stop,'.encode('utf-8'), response=True)
                print("stop measuring from", address)
            if command.strip().lower() == 'resume':
                await client.write_gatt_char(send_uuid, 'resume,'.encode('utf-8'), response=True)
                # await client.write_gatt_char(send_uuid, 'resume,0,0,0,'.encode('utf-8'), response=True)
                print("stop measuring from", address)
            if command.strip().lower() == 'led':
                await client.write_gatt_char(send_uuid, 'led,'.encode('utf-8'), response=True)
                print("toggled led on", address)
            if command.strip().lower() == 'quit':
                # await client.stop_notify(UUID)
                # await client.disconnect()
                # print("disconnect from", address)
                # break

                await client.write_gatt_char(send_uuid, 'stop,'.encode('utf-8'), response=True)
                await asyncio.sleep(5.0)
                await client.write_gatt_char(send_uuid, 'disconnect,'.encode('utf-8'), response=True)
                await asyncio.sleep(5.0)
                print("quit from", address)
                sys.exit()
                break


async def main():
    await connect(address)


if __name__ == "__main__":
    asyncio.run(main())