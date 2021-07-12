import pycom 
import ubinascii
from network import Bluetooth
import time

bt = Bluetooth()
bt.start_scan(10)

while bt.isscanning():
  adv = bt.get_adv()
  if adv:
      print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
      service_data = bt.resolve_adv_data(adv.data, Bluetooth.ADV_SERVICE_DATA)
      print(ubinascii.hexlify(service_data))
