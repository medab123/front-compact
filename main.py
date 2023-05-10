import utime
import ujson
import urequests
import _thread
from machine import Pin

led = Pin(2, Pin.OUT)
button = Pin(15, Pin.IN)

fp_name = "fp-01"

data_saved = []

def resetCounter():
    print("Sending data...")
    res = urequests.post(
        "http://10.80.0.34:8000/resetCounter",
        headers={'content-type': 'application/json'},
        data=ujson.dumps({"fp_name":fp_name}))
    print(res.text)
    
def sendData(data1):
    try:
        if data_saved:
            print(data_saved)
        print("Sending data...")
        res = urequests.post(
            "http://10.80.0.34:8000/saveData",
            headers={'content-type': 'application/json'},
            data=ujson.dumps(data1))
        print(res.text)
        if res.status_code == 200 and data_saved:
            sendSavedData()

    except OSError as e:
        if e.args[0] == 113:
            print("Connection aborted. Saving data...")
            data_saved.append(data1)
    except Exception as ex:
        print("Error: ", ex)

def sendSavedData():
    while data_saved:
        print("try to send backuped data")
        data_batch = data_saved.copy()
        data_saved.clear()
        res = urequests.post(
            "http://10.80.0.34:8000/saveData",
            headers={'content-type': 'application/json'},
            data=ujson.dumps(data_batch))
        print(res.text)

def calcDuration():
    
    print("Calculating duration...")
    while True :
        if button.value() == 0:
            led.value(1)
            sleep(0.2)
            current_time = utime.localtime()
            formatted_time = "{:02d}/{:02d}/{} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4],current_time[5])
            print(formatted_time)
            start_time = utime.time()
            while button.value() == 0:
                continue
            led.value(0)
            end_time = utime.time()
            duration = end_time - start_time
            print("Duration:", duration)
            
            data = {"start_date":formatted_time,"duration":duration,"fp_name":fp_name}
            _thread.start_new_thread(sendData, (data,))
            
            
            
# Start the calcDuration function in a new thread
_thread.start_new_thread(calcDuration, ())
