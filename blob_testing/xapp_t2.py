
import xapp_sdk as ric
import time
import os
import pdb
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json



# Azure Storage Account Configuration
STORAGE_ACCOUNT_NAME = "datalakefv41bzh"
STORAGE_ACCOUNT_KEY = "XHQUVfRfT48BfBe8BKJVuqTQUh08xRHUrAxin8ys7uoQ8MfHgP2dDVVL6DErBZWL/ZZ4qnga6xWI+ASt1vRXYg=="
CONTAINER_NAME = "bubble-mac"
BLOB_NAME="logs_mikel.json"
# Initialize the Blob Service Client
blob_service_client = BlobServiceClient(account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net", credential=STORAGE_ACCOUNT_KEY)

log_buffer = []

# Function to send data to Azure Blob Storage
# def send_to_blob_storage(event_data):
#     container_client = blob_service_client.get_container_client(CONTAINER_NAME)

#     # Define the blob name (unique per file)
#     blob_name = f"mac_log_{time.time()}.json"

#     # Upload the event data to Blob Storage as a JSON file
#     blob_client = container_client.get_blob_client(blob_name)
#     blob_client.upload_blob(json.dumps(event_data), overwrite=True)

#     print(f"Data uploaded to Blob Storage with blob name: {blob_name}")


def append_to_blob():
    
    global log_buffer
    if not log_buffer:
        print("No logs to upload.")
        return

    # Convert buffer to JSON format
    log_content = json.dumps(log_buffer, indent=2)

    # Upload entire buffer to Blob Storage
    blob_client = blob_service_client.get_blob_client(CONTAINER_NAME, BLOB_NAME)

    try:
        blob_client.upload_blob(log_content, overwrite=True)
        print(f"ALL LOGS UPLOADED TO {BLOB_NAME}")
    except Exception as e:
        print(f"Error uploading log data: {e}")   

####################
#### MAC INDICATION CALLBACK
####################

class MACCallback(ric.mac_cb):
    def __init__(self):
        ric.mac_cb.__init__(self)
        self.mac_data = []  

    # def handle(self, ind):
    #     if len(ind.ue_stats) > 0:
    #         t_now = time.time_ns() / 1000.0
    #         t_mac = ind.tstamp / 1.0
    #         t_diff = t_now - t_mac
    #         print(f'MAC Indication tstamp = {t_mac} latency = {t_diff} μs')

    def handle(self, ind):
        if len(ind.ue_stats) > 0:
            t_now = time.time_ns() / 1000.0
            t_mac = ind.tstamp / 1.0
            t_diff = t_now - t_mac
            print(f'MAC tstamp = {t_mac} latency = {t_diff} μs')

            
            event_data = {
                "type": "MAC",
                "tstamp": t_mac,
                "latency": t_diff
            }
            self.mac_data.append(event_data)
            log_buffer.append(event_data)

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
                "tstamp": t_rlc,
                "latency": t_diff
            }
            self.rlc_data.append(event_data)
            log_buffer.append(event_data)

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
                "tstamp": t_pdcp,
                "latency": t_diff
            }
            self.pdcp_data.append(event_data)
            log_buffer.append(event_data)

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
                "tstamp": t_gtp,
                "latency": t_diff
            }
            self.gtp_data.append(event_data)
            log_buffer.append(event_data)


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

####################
#### RLC INDICATION
####################

rlc_hndlr = []
for i in range(0, len(conn)):
    rlc_cb = RLCCallback()
    hndlr = ric.report_rlc_sm(conn[i].id, ric.Interval_ms_1, rlc_cb)
    rlc_hndlr.append(hndlr) 
    time.sleep(1)

####################
#### PDCP INDICATION
####################

pdcp_hndlr = []
for i in range(0, len(conn)):
    pdcp_cb = PDCPCallback()
    hndlr = ric.report_pdcp_sm(conn[i].id, ric.Interval_ms_1, pdcp_cb)
    pdcp_hndlr.append(hndlr) 
    time.sleep(1)

####################
#### GTP INDICATION
####################

gtp_hndlr = []
for i in range(0, len(conn)):
    gtp_cb = GTPCallback()
    hndlr = ric.report_gtp_sm(conn[i].id, ric.Interval_ms_1, gtp_cb)
    gtp_hndlr.append(hndlr)
    time.sleep(1)

time.sleep(10)


### End

for i in range(0, len(mac_hndlr)):
    ric.rm_report_mac_sm(mac_hndlr[i])

for i in range(0, len(rlc_hndlr)):
    ric.rm_report_rlc_sm(rlc_hndlr[i])

for i in range(0, len(pdcp_hndlr)):
    ric.rm_report_pdcp_sm(pdcp_hndlr[i])

for i in range(0, len(gtp_hndlr)):
    ric.rm_report_gtp_sm(gtp_hndlr[i])


# Avoid deadlock. ToDo revise architecture 
while ric.try_stop == 0:
    time.sleep(1)

append_to_blob()

print("Test finished")






