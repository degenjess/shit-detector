from flask import Flask, jsonify
import subprocess
import threading
import requests
import os

app = Flask(__name__)

PI_IP = "YOUR_PI_IP"

def play_alarm():
    subprocess.run(['afplay', 'PATH_TO_YOUR_VOICE_FILE'])
    subprocess.run(['afplay', 'PATH_TO_YOUR_SIREN_FILE'])
    subprocess.run(['afplay', 'PATH_TO_YOUR_LAUNCH_FILE'])

def download_photo():
    try:
        url = f"http://{PI_IP}:8080/detected_token.jpg"
        r = requests.get(url, timeout=5)
        with open('PATH_TO_YOUR_TOKEN_IMAGE/tok.png', 'wb') as f:
            f.write(r.content)
        print("Photo downloaded!")
    except Exception as e:
        print(f"Photo error: {e}")

def launch_token():
    download_photo()
    os.system('python3 PATH_TO_YOUR_SCRIPTS/launch_token.py')

@app.route('/shit_detected', methods=['POST'])
def shit_detected():
    print("\n" + "="*50)
    print("SHIT DETECTED! LAUNCHING TOKEN!")
    print("="*50 + "\n")
    threading.Thread(target=play_alarm).start()
    threading.Thread(target=launch_token).start()
    return jsonify({"status": "token_launching"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    print("Shit Detector Server started!")
    print("Waiting for signal...")
    app.run(host='0.0.0.0', port=5001)
