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
#### GTP INDICATION CALLBACK
####################

# Create a callback for GTP which derived it from C++ class gtp_cb
class GTPCallback(ric.gtp_cb):
    def __init__(self):
        # Inherit C++ gtp_cb class
        ric.gtp_cb.__init__(self)
        self.gtp_data=[]
    # Create an override C++ method 
    def handle(self, ind):
        if len(ind.gtp_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_gtp = ind.tstamp / 1.0
            t_diff = t_now - t_gtp
            print('GTP Indication tstamp = ' + str(ind.tstamp) + ' diff = ' + str(t_diff) + ' μs')          

            event_data = {
                "type": "GTP",
                "tstamp": datetime.utcnow().isoformat(),
                "latency": t_diff
            }
            json_data = json.dumps(event_data)

            try:
                with producer:
                    event_data_batch = producer.create_batch()
                    event_data_batch.add(EventData(json_data))
                    producer.send_batch(event_data_batch)
                print("Sent GTP data to Azure Event Hub:", event_data)
            except Exception as e:
                print(f"Error sending GTP data to Event Hub: {e}")



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
#### GTP INDICATION
####################

gtp_hndlr = []
for i in range(0, len(conn)):
    gtp_cb = GTPCallback()
    hndlr = ric.report_gtp_sm(conn[i].id, ric.Interval_ms_1, gtp_cb)
    gtp_hndlr.append(hndlr)
    time.sleep(1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping xApp...")


for i in range(0, len(gtp_hndlr)):
    ric.rm_report_gtp_sm(gtp_hndlr[i])

print("xAPP stopped")
