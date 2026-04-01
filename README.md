# 🌾 Sentinel-X: Advanced IoT Wildlife Intrusion & Analytics Shield
**"The Digital Scarecrow: A Cloud-Integrated Edge Computing Solution for Smart Agriculture"**

---

### 📖 Executive Summary
Sentinel-X solves the problem of **Crop Loss** and **Alarm Fatigue**. 
By utilizing **Edge Computing** (Arduino) to filter false positives and **Cloud Integration** (AWS) for long-term data persistence, 
it provides farmers with a reliable, 24/7 monitoring solution.

### 🛡️ Core Logic: Dual-Threshold Verification
Unlike basic motion sensors, Sentinel-X employs a **Verification Algorithm**:
1. **Passive Infrared (PIR):** Detects the thermal signature of a moving body.
2. **Ultrasonic (HC-SR04):** Validates the physical presence and distance of the intruder.
*If and only if both sensors trigger, the system initiates the deterrent and logs the event to the cloud.*

---

### 📊 System Integration & Connectivity
This table outlines the hardware-to-software handshake that makes Sentinel-X a "Full-Stack" IoT project.

| Component | Interface | Target | Purpose |
| :--- | :--- | :--- | :--- |
| **PIR & Ultrasonic** | Analog/Digital | Arduino Uno | Raw data collection & signal processing. |
| **Arduino Uno** | Serial (USB) | Python Bridge | Sends formatted strings (Intrusion Detected!). |
| **Python Bridge** | Boto3 Library | AWS S3 Bucket | Securely uploads logs as `.txt` files. |
| **AWS S3** | Cloud Storage | Streamlit App | Acts as a centralized data vault for the UI. |
| **Streamlit UI** | Web Interface | End User | Displays IST-synced analytics & graphs. |

---

### 🏗️ Technical Architecture
* **Edge Layer:** Arduino C++ logic for real-time deterrence (Buzzer/LED).
* **Gateway Layer:** Python script running on a 4GB RAM local host, acting as the secure bridge.
* **Cloud Layer:** AWS S3 hosting persistent telemetry data.
* **Application Layer:** Streamlit dashboard for data visualization and "Universe" themed UI.

---

### 📂 Repository Roadmap
* 📂 **`hardware/`**: Contains `sentinel_x.ino` and Tinkercad circuit schematics.
* 📂 **`software/`**: Contains `bridge.py` (Cloud Gateway) and `app.py` (Streamlit Dashboard).
* 📂 **`docs/`**: Technical project report (PDF) with the first-page privacy sanitization.
* 📂 **`config/`**: (Ignored by Git) Local environment variables for AWS IAM keys.

---

### 🔧 Installation
1. **Hardware:** Follow the pin-out mapping in `/hardware/schematic.png`.
2. **Environment:** Create a `config.py` with your AWS credentials.
3. **Execution:** ```bash
   pip install -r software/requirements.txt
   python software/bridge.py
   streamlit run software/app.py
