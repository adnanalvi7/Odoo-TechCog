# attendance_sender.py
import requests
from zk import ZK
from datetime import datetime

# Set up connection to the biometric device
BIOMETRIC_DEVICE_IP = '192.168.1.201'
API_URL = "https://adnanalvi7-odoo-techcog.odoo.com/biometric/attendance"  # Odoo API endpoint

zk = ZK(BIOMETRIC_DEVICE_IP, port=4370, timeout=10)
conn = zk.connect()

if conn:
    logs = conn.get_attendance()
    for log in logs:
        data = {
            "employee_id": log.user_id,  # Assuming `user_id` matches the biometric employee ID
            "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": 'in' if log.status == 0 else 'out',
        }
        response = requests.post(API_URL, json=data)
        print(response.json())  # Log response
else:
    print("Connection to the biometric device failed.")
