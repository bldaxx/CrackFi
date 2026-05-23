# CrackFi 🔐

**Version:** `1.0.0v`

---

## 📌 Overview

**CrackFi** is a Python-based desktop application built using the `pywifi` library that provides a clean and modern graphical user interface (GUI) for Wi-Fi network analysis.

It allows users to dynamically scan nearby networks, view comprehensive security details, and evaluate password strength using a wordlist file.

The application features multi-threading to ensure the interface remains completely responsive during active operations, alongside real-time progress tracking and precise estimated time remaining.

---

# ✨ Features

### 🔍 Dynamic Wi-Fi Scanning
Scans and updates available nearby networks automatically without freezing the user interface.

### 📊 Comprehensive Network Details
Retrieves essential intelligence including:
- SSID
- MAC Address (BSSID)
- Exact encryption type
- Signal strength (dBm)

### ⏳ Advanced Time Estimation
Computes and displays the remaining time dynamically based on actual trial speeds.

### 📈 Smooth Continuous Progress Bar
Features a modern ultra-thin progress bar design inspired by video players:
- Completely smooth
- No block divisions
- No internal text overlaps

### 🏁 Intelligent State Freeze
The progress bar freezes exactly at the correct password location upon a successful match instead of jumping directly to 100%.

### 💻 Responsive Architecture
Built with custom components:
- Entry
- Button
- Label
- ProgressBar
- ListView

Powered by `WorkerThread` processing to keep the application stable and fluid.

---

# 🛠️ Requirements & Installation

## 1. Prerequisites

- **Python:** Version `3.10+`
- **Hardware:** Compatible wireless network interface card (Wi-Fi Adapter)

---

## 2. Dependencies

Install the required libraries:

```bash
pip install PyQt6 pywifi
```

---

# 🚀 Detailed Usage Guide

To perform an authorized security evaluation on your wireless network:

### 1️⃣ Scan the Environment
Click the **Scan** button to discover surrounding networks.

### 2️⃣ Select Target Network
Type the network:
- Number (ID)
- Or exact SSID name

into the upper input field.

### 3️⃣ Analyze Security Info
Click **Get Information** to retrieve:
- Security configuration
- Signal status
- Encryption type

### 4️⃣ Load Password File
Click **Browse** and choose your password list `.txt` file.

### 5️⃣ Execute Evaluation
Click **Crack Wi-Fi** to begin the automated password evaluation process.

---

## 💡 Tip

You can monitor:
- Tried combinations in the **Terminal Output**
- Progress percentage
- Countdown timer

directly from the main interface.

---

# 📂 Project Structure

```bash
CrackFi/
│
├── main.py           # Core application execution code
├── hacklore.py       # Custom UI framework library
├── passwords.txt     # Sample evaluation wordlist file
└── README.md         # Full project documentation
```

---

# 📸 Suggested Gallery (Screenshots)

### 🖥️ Main Interface
Showing the dynamic wireless network lookup list.

### 📡 Network Intelligence View
Displaying:
- BSSID
- Cipher type
- dBm signal strength

### ⚙️ Active Processing Status
Visualizing:
- Thin smooth progress bar
- Real-time countdown timer

---

# ⚠️ Legal & Security Disclaimer

> 🛑 **IMPORTANT NOTICE**
>
> This software is strictly developed for:
>
> - Educational purposes
> - Research
> - Authorized security testing
> - Ethical hacking
> - Authorized network auditing
>
> Running this tool against any wireless infrastructure without explicit written permission from the rightful owner is illegal.
>
> Unauthorized usage may violate local cybercrime laws and regulations and could expose the user to severe legal consequences.
>
> The developer assumes absolutely no liability and is not responsible for any misuse, damage, or legal issues caused by this application.

---

# 📜 License

This project is intended for educational and authorized security research purposes only.
