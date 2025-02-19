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
#### PDCP INDICATION CALLBACK
####################

class PDCPCallback(ric.pdcp_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.pdcp_cb.__init__(self)
        self.pdcp_data=[]
   # Override C++ method: virtual void handle(swig_pdcp_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_pdcp_ind_msg_t
        if len(ind.rb_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_pdcp = ind.tstamp / 1.0
            t_diff = t_now - t_pdcp
            print('PDCP Indication tstamp = ' + str(ind.tstamp) + ' latency = ' + str(t_diff) + ' μs')

            event_data = {
                "type": "PDCP",
                "tstamp": datetime.utcnow().isoformat(),
                "latency": t_diff
            }
            json_data = json.dumps(event_data)

            try:
                with producer:
                    event_data_batch = producer.create_batch()
                    event_data_batch.add(EventData(json_data))
                    producer.send_batch(event_data_batch)
                print("Sent PDCP data to Azure Event Hub:", event_data)
            except Exception as e:
                print(f"Error sending PDCP data to Event Hub: {e}")


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
#### PDCP INDICATION
####################

pdcp_hndlr = []
for i in range(0, len(conn)):
    pdcp_cb = PDCPCallback()
    hndlr = ric.report_pdcp_sm(conn[i].id, ric.Interval_ms_1, pdcp_cb)
    pdcp_hndlr.append(hndlr) 
    time.sleep(1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping xApp...")


for i in range(0, len(pdcp_hndlr)):
    ric.rm_report_pdcp_sm(pdcp_hndlr[i])

print("xAPP stopped")

