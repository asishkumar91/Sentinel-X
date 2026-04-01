import serial
import boto3
import time

# 1. Configuration
ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
BUCKET_NAME = "your-sentinel-x-bucket-name"
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# 2. Arduino Serial Connection
ser = serial.Serial('COM3', 9600, timeout=1) 

current_incident_data = []
last_alert_time = 0
COOLDOWN_SECONDS = 10 

print("--- PROJECT: LIVE CLOUD GATEWAY ---")

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        
        if "ALARM!" in line:
            print(f"📡 SENSOR ACTIVE: {line}")
            current_incident_data.append(f"{time.strftime('%H:%M:%S')} - {line}")
            last_alert_time = time.time()

    # LOGIC: If animal is gone for 10 seconds, UPLOAD and SHOW OUTPUT
    if current_incident_data and (time.time() - last_alert_time > COOLDOWN_SECONDS):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"incident_{timestamp}.txt"
        content = "\n".join(current_incident_data)
        
        try:
            # UPLOAD PROCESS
            s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=content)
            
            # OUTPUT CONFIRMATION (Like check_cloud.py)
            print("-" * 40)
            print(f"✅ CLOUD SYNC SUCCESSFUL!")
            print(f"📄 File Name: {filename}")
            print(f"📊 Data Points Captured: {len(current_incident_data)}")
            print(f"🔗 View at: https://s3.console.aws.amazon.com/s3/buckets/{BUCKET_NAME}")
            print("-" * 40)
            
            current_incident_data = [] # Reset for next animal
        except Exception as e:
            print(f"❌ CLOUD ERROR: {e}")