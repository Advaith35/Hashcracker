# 🔒 Hash Cracker with AI Analysis

A modern hash cracking tool with integrated AI-powered security analysis, featuring multiple input methods and real-time substitution of cracked hashes.

## Demo Video

Here's a quick demonstration of the Hash Cracker Pro in action:

![Demo](https://raw.githubusercontent.com/Advaith35/Hashcracker/main/hashcracker.gif)

You can see how it quickly cracks the MD5 hash and displays the result.

## Features

- **Multi-API Cracking Engine**
    - Supports MD5, SHA1, SHA256, SHA384, SHA512
    - Integrates with 4 different hash databases
- **Smart Input Handling**
    - Single hash input
    - File upload (TXT, CSV, LOG, MD, JSON)
    - Direct text paste with auto-hash detection
- **AI-Powered Analysis**
    - Gemini API integration for security assessments
    - Context-aware vulnerability reporting
- **Enhanced Visualization**
    - Dark theme UI with custom styling
    - In-place hash substitution display
    - Progress tracking and status indicators
- **Export Capabilities**
    - Download processed results
    - Copy-to-clipboard functionality

## 🚀 Installation

1. Clone the repository:
```
git clone [https://github.com/Advaith35/Hashcracker.git](https://github.com/Advaith35/Hashcracker.git)
cd hash-cracker
```
Install dependencies:
```

pip install streamlit requests websocket-client google-generativeai
```
Get a Google Gemini API Key and add it to hash_cracker.py:
Python
```
GEMINI_API_KEY = "your-api-key-here"  # Line 16
```
🖥️ Usage
Start the application:

```

streamlit run hash_cracker.py
```
Input Methods:

Single Hash Directly enter any 32-128 character hash
File Upload Process documents containing multiple hashes
Text Paste Analyze raw text with embedded hashes
Example Hashes:

MD5: 5f4dcc3b5aa765d61d8327deb882cf99 (password)
SHA1: a94a8fe5ccb19ba61c4c0873d391e987982fbbd3 (test)
⚙️ Configuration
Configure in hash_cracker.py:

Python
```

# API Configurations (Line 15-16)
GEMINI_API_KEY = "your-api-key-here"  # Required for AI analysis

# WebSocket Config (Line 60-61)
websocket.create_connection("wss://md5hashing.net/...")  # Update if needed

# API Endpoints (Line 83-113)
# Modify alpha/beta/gamma/theta functions as needed
```
📊 Sample Output
Processed Content:
```
User Database:
admin:password → [password]
backup:7c4a8d09ca3762af61e59520943dc26494f8941b → [❌7c4a8d...❌]
```
Security Assessment:
```
The cracked password 'password' for admin represents critical vulnerability (Common Credential #1). 
Uncracked SHA1 hash suggests better security for backup account, but recommend rotating all credentials 
and enforcing complexity requirements (12+ chars, special characters).
```

⚠️ Disclaimer
This tool is intended for:

Educational purposes
Security auditing (authorized systems only)
Password recovery (personal accounts)
Never use for:

Unauthorized system access
Illegal activities
Malicious purposes
Effectiveness depends on external API availability. Some services may require accounts or have rate limits.

📜 License
MIT License - See LICENSE for details
