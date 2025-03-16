import streamlit as st
import re
import urllib3
import requests
import websocket
from io import StringIO
import google.generativeai as genai

# Add this at the top with other configurations
GEMINI_API_KEY = "AIzaSyCPJQ74qSRKVnM7ktYv0d_dF1eOxOdVW7U"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure Streamlit page
st.set_page_config(page_title="Hash Cracker", page_icon="🔒", layout="wide")

# Custom CSS styling
st.markdown("""
<style>
    .stTextInput input {background-color: #f0f2f6;}
    .stTextArea textarea {background-color: #f0f2f6;}
    .result-box {padding: 20px; background-color: #e8f4fc; border-radius: 5px; margin: 10px 0;}
    .stProgress > div > div > div > div {background-color: #4CAF50;}
</style>
""", unsafe_allow_html=True)

# API Functions
def alpha(hashvalue, hashtype):
    try:
        cookies = {'ASP.NET_SessionId': 'be2jpjuviqbaa2mmq1w4h5ci'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'}
        data = {
            '__EVENTTARGET': 'Button1',
            '__VIEWSTATE': '6fEUcEEj0b0eN1Obqeu4TSsOBdS0APqz...',
            'ctl00$ContentPlaceHolder1$TextBoxInput': hashvalue,
            'ctl00$ContentPlaceHolder1$InputHashType': hashtype,
        }
        response = requests.post('https://www.cmd5.org/', cookies=cookies, 
                               headers=headers, data=data, timeout=10)
        match = re.search(r'<span id="LabelAnswer"[^>]+?>(.+)</span>', response.text)
        return match.group(1) if match else None
    except Exception as e:
        return None

def beta(hashvalue, hashtype):
    try:
        ws = websocket.create_connection("wss://md5hashing.net/sockjs/697/etstxji0/websocket")
        connect_msg = r'["{\"msg\":\"connect\",\"version\":\"1\",\"support\":[\"1\",\"pre2\",\"pre1\"]}"]'
        ws.send(connect_msg)
        ws.recv()

        method_msg = r'["{\"msg\":\"method\",\"method\":\"hash.get\",\"params\":[\"%s\",\"%s\"],\"id\":\"1\"}"]' % (
            hashtype, hashvalue)
        ws.send(method_msg)
        response = ws.recv()
        ws.close()

        match = re.search(r'"value\\":\\([^,]+)', response)
        return match.group(1)[1:-1] if match else None
    except Exception as e:
        return None

def gamma(hashvalue, hashtype):
    try:
        response = requests.get(f'https://www.nitrxgen.net/md5db/{hashvalue}', 
                              timeout=5, verify=False)
        return response.text if response.text else None
    except:
        return None

def theta(hashvalue, hashtype):
    try:
        url = f'https://md5decrypt.net/Api/api.php?hash={hashvalue}&hash_type={hashtype}'\
              '&email=noyile6983@lofiey.com&code=fa9e66f3c9e245d6'
        response = requests.get(url, timeout=5)
        return response.text if response.text else None
    except:
        return None

# Core Cracking Logic
def detect_hash_type(hashvalue):
    length = len(hashvalue)
    return {
        32: 'md5',
        40: 'sha1',
        64: 'sha256',
        96: 'sha384',
        128: 'sha512'
    }.get(length, None)

def crack_hash(hashvalue):
    hash_type = detect_hash_type(hashvalue)
    if not hash_type:
        return "Unsupported hash type"
    
    apis = {
        'md5': [gamma, alpha, beta, theta],
        'sha1': [alpha, beta, theta],
        'sha256': [alpha, beta, theta],
        'sha384': [alpha, beta, theta],
        'sha512': [alpha, beta, theta]
    }
    
    for api in apis.get(hash_type, []):
        try:
            result = api(hashvalue, hash_type)
            if result and result not in ["", "Not found"]:
                return result
        except:
            continue
    return "Not found"

# Streamlit UI
def main():
    st.title("🔒 Hash Cracker")
    
    # Initialize session state variables
    if 'original_content' not in st.session_state:
        st.session_state.original_content = None
    if 'processed_content' not in st.session_state:
        st.session_state.processed_content = None
    
    # Input method selection
    input_method = st.radio(
        "Select input method:",
        ["Single Hash", "File Upload", "Paste Text"],
        horizontal=True,
        key='input_method'
    )
    
    hashes_to_crack = set()
    original_content = None
    
    # Input handling section
    with st.container(border=True):
        if input_method == "Single Hash":
            hash_input = st.text_input(
                "Enter hash:", 
                placeholder="e.g., 5f4dcc3b5aa765d61d8327deb882cf99",
                key='single_hash'
            )
            if hash_input:
                hashes_to_crack.add(hash_input.strip())
        
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload file with hashes", 
                type=["txt", "csv", "log", "md", "json"],
                key='file_upload'
            )
            if uploaded_file:
                original_content = uploaded_file.getvalue().decode()
                st.session_state.original_content = original_content
                hashes_to_crack.update(re.findall(
                    r"[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}",
                    original_content, 
                    re.IGNORECASE
                ))
        
        elif input_method == "Paste Text":
            paste_text = st.text_area(
                "Paste text containing hashes", 
                height=150,
                key='paste_text'
            )
            if paste_text:
                original_content = paste_text
                st.session_state.original_content = original_content
                hashes_to_crack.update(re.findall(
                    r"[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}",
                    paste_text, 
                    re.IGNORECASE
                ))
    
    # Processing section
    if st.button("🔑 Crack & Analyze", use_container_width=True):
        if not hashes_to_crack:
            st.error("Please provide some hashes to crack!")
            return
        
        results = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total_hashes = len(hashes_to_crack)
        for i, hashvalue in enumerate(hashes_to_crack):
            status_text.info(f"🔍 Processing {i+1}/{total_hashes}: {hashvalue}")
            results[hashvalue] = crack_hash(hashvalue)
            progress_bar.progress((i+1)/total_hashes)
        
        if results:
            success_count = sum(1 for v in results.values() if v != "Not found")
            st.success(f"✅ Cracked {success_count}/{total_hashes} hashes!")
            
            # Handle different display modes
            if input_method != "Single Hash" and st.session_state.original_content:
                # Create substituted content
                substituted = st.session_state.original_content
                for hash_val, plain in results.items():
                    replacement = f"[{plain}]" if plain != "Not found" else f"❌{hash_val}❌"
                    substituted = substituted.replace(hash_val, replacement)
                
                st.session_state.processed_content = substituted
                
                # Display processed content
                st.subheader("Processed Content")
                st.markdown(f"""
                <div class="result-box" style="white-space: pre-wrap;">
                    {substituted}
                </div>
                """, unsafe_allow_html=True)
                
                # Gemini analysis
                with st.spinner("🔮 Generating security assessment..."):
                    try:
                        analysis = process_with_gemini(
                            st.session_state.original_content,
                            st.session_state.processed_content
                        )
                        st.subheader("Security Assessment")
                        st.markdown(f"""
                        <div class="result-box" style="background-color: #fff3cd;">
                            {analysis}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Failed to generate analysis: {str(e)}")
            
            else:  # Single hash mode
                for hash_value, plaintext in results.items():
                    # Display result
                    st.markdown(f"""
                    <div class="result-box">
                        <strong style="font-size: 18px">{hash_value}</strong> → 
                        <span style="color:#28a745; font-weight: bold; font-size: 16px">
                            {plaintext if plaintext != "Not found" else "❌ Not Found"}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Individual analysis for single hash
                    if plaintext != "Not found":
                        with st.spinner("🔍 Generating analysis..."):
                            analysis = process_with_gemini(hash_value, plaintext)
                            st.markdown(f"""
                            <div class="result-box" style="margin-top: 8px;">
                                📌 <strong>Analysis:</strong> {analysis}
                            </div>
                            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No hashes could be cracked")

    # Show download button for processed content
    if st.session_state.processed_content:
        st.download_button(
            label="📥 Download Processed Content",
            data=st.session_state.processed_content,
            file_name="processed_content.txt",
            mime="text/plain",
            use_container_width=True
        )

def process_with_gemini(original_text, substituted_text):
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Analyze this security transformation:
        
        Original Content:
        {original_text}
        
        Substituted Content (hashes replaced):
        {substituted_text}
        
        Provide a brief security assessment in 2-3 sentences focusing on password strength 
        and potential vulnerabilities revealed by the substitutions."""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Gemini Analysis Error: {str(e)}"

# Modified display function
st.markdown("""
<style>
    .stTextInput input {background-color: #404040; color: #ffffff;}
    .stTextArea textarea {background-color: #404040; color: #ffffff;}
    .result-box {
        padding: 20px; 
        background-color: #2d2d2d;
        border-radius: 5px; 
        margin: 10px 0;
        color: #e0e0e0;
        border: 1px solid #404040;
    }
    .stProgress > div > div > div > div {background-color: #28a745;}
    .st-bb {background-color: #1a1a1a;}
    .st-at {background-color: #1a1a1a;}
    .st-cj {color: #ffffff;}
</style>
""", unsafe_allow_html=True)
# Modified display_results function
def display_results(results, original_content=None):
    if original_content:  # For file/text paste input
        # ... [previous content substitution code remains the same] ...
        
        st.subheader("Processed Content")
        st.markdown(f"""
        <div class="result-box" style="white-space: pre-wrap; background-color: #363636; color: #d0d0d0;">
            {substituted}
        </div>
        """, unsafe_allow_html=True)
        
        # Gemini analysis
        with st.spinner("🔮 Generating security assessment..."):
            try:
                analysis = process_with_gemini(
                    st.session_state.original_content,
                    st.session_state.processed_content
                )
                st.subheader("Security Assessment")
                st.markdown(f"""
                <div class="result-box" style="background-color: #424242; border-color: #28a745;">
                    <span style="color: #a0d0ff">{analysis}</span>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate analysis: {str(e)}")
    
    else:  # For single hash input
        for hash_value, plaintext in results.items():
            st.markdown(f"""
            <div class="result-box" style="background-color: #363636;">
                <strong style="font-size: 18px; color: #ffffff">{hash_value}</strong> → 
                <span style="color:#28a745; font-weight: bold; font-size: 16px">
                    {plaintext if plaintext != "Not found" else "❌ Not Found"}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            if plaintext != "Not found":
                with st.spinner("🔍 Generating analysis..."):
                    analysis = process_with_gemini(hash_value, plaintext)
                    st.markdown(f"""
                    <div class="result-box" style="margin-top: 8px; background-color: #424242;">
                        <span style="color: #c0c0c0">📌 <strong>Analysis:</strong></span> 
                        <span style="color: #d0d0d0">{analysis}</span>
                    </div>
                    """, unsafe_allow_html=True)


# ... (rest of the code remains the same)

if __name__ == "__main__":
    main()