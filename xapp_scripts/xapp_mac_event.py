
import xapp_sdk as ric
import time
import os
import pdb
from datetime import datetime

from azure.eventhub import EventHubProducerClient, EventData
import json



# Azure EVENT-HUB
EVENT_HUB_NAME = "bubble-eventtest"
EVENT_HUB_CONNECTION_STRING = "Endpoint=sb://bubble-event.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ithTuhFlPGwr1ZNOyZ17HLPmdgjZ34rXY+AEhLfiqdI="

# Initialize the Event Hub Producer Client
producer = EventHubProducerClient.from_connection_string(
    EVENT_HUB_CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME
)

####################
#### MAC INDICATION CALLBACK
####################

class MACCallback(ric.mac_cb):
    def __init__(self):
        ric.mac_cb.__init__(self)
        self.mac_data = []  


    def handle(self, ind):
        if len(ind.ue_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_mac = ind.tstamp / 1.0
            t_diff = t_now - t_mac
            print(f'MAC tstamp = {t_mac} latency = {t_diff} μs')

            
            event_data = {
                "type": "MAC",
                "tstamp": datetime.utcnow().isoformat(),
                "latency": t_diff
            }
            json_data = json.dumps(event_data)

            try:
                with producer:
                    event_data_batch = producer.create_batch()
                    event_data_batch.add(EventData(json_data))
                    producer.send_batch(event_data_batch)
                print("Sent MAC data to Azure Event Hub:", event_data)
            except Exception as e:
                print(f"Error sending MAC data to Event Hub: {e}")



####################
####  GENERAL 
####################

ric.init()

conn = ric.conn_e2_nodes()
assert(len(conn) > 0)
for i in range(0, len(conn)):
    print("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
    print("Global E2 Node [" + str(i) + "]: PLMN MNC = " + str(conn[i].id.plmn.mnc))

####################
#### MAC INDICATION
####################

mac_hndlr = []
for i in range(0, len(conn)):
    mac_cb = MACCallback()
    hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_1, mac_cb)
    mac_hndlr.append(hndlr)     
    time.sleep(1)





try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping xApp...")

### End

for i in range(0, len(mac_hndlr)):
    ric.rm_report_mac_sm(mac_hndlr[i])




# # Avoid deadlock. ToDo revise architecture 
# while ric.try_stop == 0:
#     time.sleep(1)

print("xAPP stopped")






