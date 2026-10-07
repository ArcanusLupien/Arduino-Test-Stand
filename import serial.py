import serial
import time
import csv

# 1. Connect to Arduino (Change COM port to match your system)
# Set timeout to prevent python from locking up if data stops
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=1)
time.sleep(2) # Allow Arduino time to reset upon connection

# 2. Prepare the CSV Data Log File
with open('test_stand_log.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp_ms", "Sensor_Voltage"]) # Headers
    
    print("Test Stand Initialized. Activating valve...")
    arduino.write(b"ACTIVATE\n") # Send actuation command to hardware
    
    start_time = time.time()
    try:
        # Run test sequence for 5 seconds
        while time.time() - start_time < 5.0:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                if line:
                    data = line.split(',')
                    if len(data) == 2:
                        print(f"Telemetry received -> Time: {data[0]}ms, Volts: {data[1]}V")
                        writer.writerow(data) # Log data straight to disk
                        
    except KeyboardInterrupt:
        print("Test interrupted safely by user.")
    finally:
        print("Sequence complete. Deactivating valve.")
        arduino.write(b"DEACTIVATE\n")
        arduino.close()