import datetime
from epics import PV
import time


def monitor_switch_pv(switch_pv_name, count_pv_name,delay_pv_name):
    switch_pv = PV(switch_pv_name)
    count_pv = PV(count_pv_name)
    delay_pv = PV(delay_pv_name)
    
    timestamp = None
    delay_times = []
    second_timestamp = None
    def switch_pv_callback(pvname=None, value=None, **kwargs):
        nonlocal timestamp
        if value == 1: 
            timestamp = time.time()
            readable_time = datetime.datetime.utcfromtimestamp(timestamp)
            print(f"Switch PV timestamp: {readable_time}")

    def second_pv_callback(pvname=None, value=None, **kwargs):
        nonlocal second_timestamp
        second_timestamp = time.time()
        readable_time = datetime.datetime.utcfromtimestamp(second_timestamp)
        print(f"count PV timestamp: {readable_time}")

       
        if timestamp is not None:
            delay_time = second_timestamp - timestamp
            print(f"Delay time: {delay_time:.6f} seconds")
            delay_times.append(delay_time)
            delay_pv.put(delay_time)
    switch_pv.add_callback(switch_pv_callback)
    count_pv.add_callback(second_pv_callback)

    print("Monitoring switch PV. Press Ctrl+C to exit.")
    
    try:
        while True:
            time.sleep(0.1)  
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user. Exiting...")

    return delay_times




if __name__ == "__main__":
    switch_pv_name = "13ARV020:cam1:Acquire"
    count_pv_name = "13ARV020:cam1:ArrayCounter_RBV"
    delay_pv_name = "13ARV020:cam1:Delay_EPICS_Time"
    delay_times = monitor_switch_pv(switch_pv_name, count_pv_name,delay_pv_name)
    