# AI Shit Detector — Auto Token Launcher

The world's first AI-powered fecal detection system that automatically launches a meme token on Pump.fun the moment it detects shit on camera.

---

## How It Works

1. Raspberry Pi 5 with a camera constantly monitors the scene
2. A custom-trained YOLOv8 neural network detects the target object in real time
3. When detected with sufficient confidence, Pi sends a signal to Mac over local Wi-Fi
4. Mac plays an alarm and automatically creates a token on Pump.fun
5. The token image is the actual photo captured at the moment of detection

---

## This is not ChatGPT

This is a fully autonomous edge AI system. The model was trained from scratch on a custom dataset. Everything runs locally on the device — no cloud, no API calls, no external AI services.

- Custom dataset, custom training
- YOLOv8 running on Raspberry Pi hardware
- Hailo-8L NPU available for hardware acceleration
- Browser automation handles the entire Pump.fun flow without human input

---

## Hardware

| Component | Model |
|-----------|-------|
| Single Board Computer | Raspberry Pi 5 8GB |
| AI Accelerator | Hailo-8L AI HAT+ (13 TOPS) |
| Storage | Kingston Canvas Go! Plus 128GB |
| Camera | TP-Link Tapo C110 |
| Power | Raspberry Pi 27W USB-C PSU |

---

## Project Structure

detector.py          — Pi: real-time camera monitoring and AI detection
shit_detector.py     — Mac: signal receiver, alarm, token launcher
launch_token.py      — Mac: Pump.fun browser automation via Patchright
requirements_pi.txt  — Dependencies for Raspberry Pi
requirements_mac.txt — Dependencies for Mac
---

## Setup

### Raspberry Pi

```bash
sudo apt install -y hailo-all
python3 -m venv ~/yolo_env --system-site-packages
source ~/yolo_env/bin/activate
pip install -r requirements_pi.txt
```

### Train the model

Download a dataset from Roboflow Universe in YOLOv8 format, then:

```bash
python -c "
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.train(data='data.yaml', epochs=50, imgsz=640, batch=4, device='cpu')
"
```

### Mac

```bash
pip install -r requirements_mac.txt
python3 -m patchright install chromium
```

---

## Configuration

**detector.py**
- Set `MAC_IP` to your Mac local IP address
- Set the RTSP URL with your camera credentials

**launch_token.py**
- Set `PHANTOM_DIR` to the path of your Phantom extension folder
- Set `PHANTOM_PASSWORD` to your Phantom wallet password
- Set `TOKEN_NAME`, `TOKEN_SYMBOL`, `TOKEN_DESCRIPTION`
- Cookies from pump.fun must be saved to `cookies.json` for Cloudflare bypass

**shit_detector.py**
- Set `PI_IP` to your Raspberry Pi local IP address
- Set paths to your audio files

---

## Running

On Raspberry Pi:

```bash
source ~/yolo_env/bin/activate
cd /home/pi && python3 -m http.server 8080 &
python detector.py
```

On Mac:

```bash
python3 shit_detector.py
```

---

## Model Performance

| Metric | Value |
|--------|-------|
| Training images | 934 |
| Epochs | 50 |
| mAP50 | 89.3% |
| Inference time | ~250ms on CPU |

---

## Tech Stack

- Python 3.11
- YOLOv8 by Ultralytics
- OpenCV
- Patchright
- Solana / Phantom Wallet
- Flask
- Raspberry Pi OS Bookworm 64-bit
