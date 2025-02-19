import xapp_sdk as ric
import time
import os
import pdb
from datetime import datetime

from azure.eventhub import EventHubProducerClient, EventData
import json



# Azure EVENT-HUB
EVENT_HUB_NAME = "bubble-eventtest"
EVENT_HUB_CONNECTION_STRING = "Endpoint=xxx"

# Initialize the Event Hub Producer Client
producer = EventHubProducerClient.from_connection_string(
    EVENT_HUB_CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME
)


####################
#### RLC INDICATION CALLBACK
####################

class RLCCallback(ric.rlc_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.rlc_cb.__init__(self)
        self.rlc_data = []  
    # Override C++ method: virtual void handle(swig_rlc_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_rlc_ind_msg_t
        if len(ind.rb_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_rlc = ind.tstamp / 1.0
            t_diff = t_now - t_rlc
            print('RLC Indication tstamp = ' + str(ind.tstamp) + ' latency = ' + str(t_diff) + ' μs')
                        # Collect the data in the buffer (list)
            
            event_data = {
                "type": "RLC",
                "tstamp": datetime.utcnow().isoformat(),
                "latency": t_diff
            }
            json_data = json.dumps(event_data)

            try:
                with producer:
                    event_data_batch = producer.create_batch()
                    event_data_batch.add(EventData(json_data))
                    producer.send_batch(event_data_batch)
                print("Sent RLC data to Azure Event Hub:", event_data)
            except Exception as e:
                print(f"Error sending RLC data to Event Hub: {e}")



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
#### RLC INDICATION
####################

rlc_hndlr = []
for i in range(0, len(conn)):
    rlc_cb = RLCCallback()
    hndlr = ric.report_rlc_sm(conn[i].id, ric.Interval_ms_1, rlc_cb)
    rlc_hndlr.append(hndlr) 
    time.sleep(1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping xApp...")

for i in range(0, len(rlc_hndlr)):
    ric.rm_report_rlc_sm(rlc_hndlr[i])

print("xAPP stopped")
