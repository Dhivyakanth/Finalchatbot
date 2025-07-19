import streamlit as st
import datetime
from chatbot_interactive import generate_response
import pandas as pd

# --- Festival Data (Tamil/Indian festivals) ---
FESTIVALS = [
    {"name": "Pongal", "date": "2025-01-14"},
    {"name": "Thai Poosam", "date": "2025-01-24"},
    {"name": "Maha Shivaratri", "date": "2025-02-26"},
    {"name": "Ugadi", "date": "2025-03-30"},
    {"name": "Tamil New Year", "date": "2025-04-14"},
    {"name": "Ramzan (Eid-ul-Fitr)", "date": "2025-03-31"},
    {"name": "Aadi Perukku", "date": "2025-08-03"},
    {"name": "Vinayaka Chaturthi", "date": "2025-08-27"},
    {"name": "Navaratri", "date": "2025-09-22"},
    {"name": "Ayudha Pooja", "date": "2025-10-01"},
    {"name": "Vijayadashami", "date": "2025-10-02"},
    {"name": "Deepavali", "date": "2025-10-20"},
    {"name": "Karthigai Deepam", "date": "2025-12-05"},
    {"name": "Christmas", "date": "2025-12-25"},
    {"name": "Pongal", "date": "2025-07-28"},  # Added as requested
]

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Change this to a secure password in production

# --- Predefined Questions (from sales_chatbot.py) ---
PREDEFINED_QUESTIONS = [
    "What is the total revenue from all orders?",
    "What is the average order value?",
    "How much revenue did we generate this month?",
    "What is the total quantity sold this year?",
    "How many dress orders are confirmed?",
    "How many pending or cancelled orders do we have?",
    "What is the status breakdown of all orders?",
    "What is the average rate per meter?",
    "How many premium quality orders have been made?",
    "Predict sales for premium cotton dresses",
    "Show me top 5 performing agents",
    "What is the conversion rate of orders?",
    "Which composition material sells best?",
    "What is the average quantity per order?",
    "Show me daily weave analysis",
    "What is the weekly composition breakdown?",
    "Show me monthly quality analysis",
    "What is the yearly status breakdown?",
    "Show me leading customers by month",
    "Who are the top agents weekly?",
    "Daily customer analysis",
    "Weekly agent performance",
    "Monthly weave trends",
    "Yearly composition analysis"
]

# --- Notification Helper ---
def load_sales_data():
    # Replace with your actual data loading logic
    try:
        df = pd.read_csv('sales_data.csv')  # Update with your actual file
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception:
        return None

def show_festival_notifications():
    today = datetime.date.today()
    notified = st.session_state.get('notified_festival', False)
    if notified:
        return
    st.toast("👋 Welcome, Admin! Wishing you a productive day!", icon="👋")
    for fest in FESTIVALS:
        fest_date = datetime.datetime.strptime(fest["date"], "%Y-%m-%d").date()
        days_left = (fest_date - today).days
        if 0 <= days_left <= 10:
            offer_msg = f"Upcoming Festival: {fest['name']} on {fest_date.strftime('%b %d, %Y')} ({days_left} days left)."
            msg = (
                f"🎊 {offer_msg} {fest['name']} is coming! Consider giving a discount."
            )
            st.toast(msg, icon="🎊")
    st.session_state['notified_festival'] = True

# --- Streamlit App ---
st.set_page_config(page_title="Dress Sales Monitoring Chatbot", page_icon="👗", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_response" not in st.session_state:
    st.session_state.current_response = ""

# --- Login Page ---
def login_page():
    st.markdown("""
        <div style='text-align:center; margin-top: 80px;'>
            <h1 style='color:#6C3483;'>👗 Dress Sales Monitoring Chatbot</h1>
            <h3 style='color:#2874A6;'>Admin Login</h3>
        </div>
    """, unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        login_submit = st.form_submit_button("Login", use_container_width=True, type="primary")
    if login_submit:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.just_logged_in = True  # set a flag
        else:
            st.error("Invalid credentials. Please try again.")
    # After the button, outside the if-block:
    if st.session_state.get("just_logged_in"):
        st.success("Login successful! Redirecting to chat...")
        st.session_state.just_logged_in = False

# --- Chat Page ---
def chat_page():
    st.markdown("""
        <style>
        /* Removed custom background color to use Streamlit default */
        .stChatMessage {
            background: #fff !important;
            color: #000 !important;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
            border: 1px solid #e0e0e0;
        }
        .stUser {background: #fff !important; color: #000 !important;}
        .stBot {background: #fff !important; color: #000 !important;}
        /* Predefined questions bar container */
        .predefined-bar {
            background: #fff !important;
            padding: 16px 0 8px 0;
            border-radius: 8px;
            margin-bottom: 16px;
        }
        /* Fix for predefined question buttons */
        button[data-testid^="baseButton"] {
            background: #222 !important;
            color: #fff !important;
            border: 1px solid #e0e0e0 !important;
            font-weight: 500;
            font-size: 1rem;
        }
        button[data-testid^="baseButton"]:hover {
            background: #444 !important;
            color: #fff !important;
        }
        /* Prompt bar and send button styling */
        .prompt-bar {
            background: #fff !important;
            box-shadow: 0 -2px 8px rgba(0,0,0,0.05);
            border-top: 1px solid #e0e0e0;
        }
        section[data-testid="stTextInput"] input {
            background: #fff !important;
            color: #000 !important;
            border: 1px solid #e0e0e0 !important;
        }
        button[kind="primary"], button[data-testid="baseButton-primary"] {
            background: #222 !important;
            color: #fff !important;
            border: 1px solid #e0e0e0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("👗 Dress Sales Monitoring Chatbot")
    st.caption("Ask about sales trends, product performance, or request predictions!")

    # Festival notifications
    show_festival_notifications()

    # Predefined questions
    st.markdown('<div class="predefined-bar">', unsafe_allow_html=True)
    st.markdown("**Quick Questions:**")
    q_cols = st.columns(3)
    for i, question in enumerate(PREDEFINED_QUESTIONS):
        if q_cols[i % 3].button(question, key=f"predef_{i}"):
            # Add to backend history for context
            st.session_state.chat_history.append({
                "role": "user",
                "parts": [{"text": question}]
            })
            with st.spinner("AI is thinking..."):
                ai_response = generate_response(question, st.session_state.chat_history)
            st.session_state.chat_history.append({
                "role": "model",
                "parts": [{"text": ai_response}]
            })
            st.session_state.current_response = ai_response
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input with Enter key functionality
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your question...", key="chat_input", value="", label_visibility="collapsed")
    with col2:
        send = st.button("Send", use_container_width=True, key="send_btn")
    
    # Handle Enter key and Send button
    if (send and user_input.strip()) or (user_input.strip() and user_input != st.session_state.get("last_input", "")):
        st.session_state.last_input = user_input
        # Add to backend history for context
        st.session_state.chat_history.append({
            "role": "user",
            "parts": [{"text": user_input}]
        })
        with st.spinner("AI is thinking..."):
            ai_response = generate_response(user_input, st.session_state.chat_history)
        st.session_state.chat_history.append({
            "role": "model",
            "parts": [{"text": ai_response}]
        })
        st.session_state.current_response = ai_response
        st.rerun()

    # Display only current response below the input
    if st.session_state.current_response:
        st.markdown("---")
        st.markdown("**Response:**")
        st.markdown(f"<div class='stChatMessage stBot'><b>AI:</b> {st.session_state.current_response}</div>", unsafe_allow_html=True)

# --- Main App Logic ---
if not st.session_state.logged_in:
    login_page()
else:
    chat_page() 