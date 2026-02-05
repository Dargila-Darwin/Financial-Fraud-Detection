import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import uuid

# ================= PAGE =================
st.set_page_config(layout="wide", page_title="Fraud Detection System")

st.markdown("""
<style>

/* MOVE ONLY REVIEW FRAUD ACTION UP */
.stRadio > div {
    margin-top:-12px !important;
}

/* tighten spacing under Action label */
.stRadio label {
    padding-top:2px !important;
    padding-bottom:2px !important;
}

/* MAIN BACKGROUND */
.stApp {
    background:#f5f7fb;
}

/* BANK HEADER */
.bank-header {
    background: linear-gradient(to right, #0f2a44, #0b3d91);
    padding:20px 50px;
    border-radius:0px;
    margin-bottom:10px;
    width:100%;
    border:none !important;
    box-shadow:none !important;
    /* full-bleed to remove right white gap */
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
}

/* Header contact line */
.header-contact {
    text-align: center;
    color: #cfe3ff;
    font-size: 16px;
    font-weight: 500;
    margin: 0 0 8px 0;
}

.header-contact .bank-name {
    font-weight: 700;
    color: #ffffff;
}

.header-icon {
    width: 14px;
    height: 14px;
    vertical-align: -2px;
    margin-right: 6px;
    fill: #cfe3ff;
}

.header-block {
    margin-right: 48px;
}

/* Moving header text (left to right) */
.header-ticker {
    overflow: hidden;
    white-space: nowrap;
}

.header-ticker-text {
    display: inline-flex;
    gap: 48px;
    animation: header-move 45s linear infinite;
    will-change: transform;
}

@keyframes header-move {
    0% { transform: translateX(-33.333%); }
    100% { transform: translateX(0); }
}

/* BANK TITLE */
.bank-title {
    font-size:42px;
    font-weight:900;
    color:#0b3d91;
    letter-spacing:1px;
}

/* LOGIN POPOVER */
.login-label {
    font-size: 12px;
    color: #555;
    margin: 6px 0 2px 0;
}

.login-status {
    text-align: center;
}

.login-status-title {
    font-size: 20px;
    font-weight: 700;
    margin: 0 0 2px 0;
    color: #222;
}

.login-status-role {
    font-size: 14px;
    color: #666;
    margin: 0;
}

.logout-spacer {
    height: 8px;
}

/* Login popover trigger sizing and alignment */
.login-popover-wrap {
    display: flex;
    justify-content: flex-end;
}

div[data-testid="stPopover"] button {
    font-size: 18px !important;
    padding: 10px 16px !important;
    border-radius: 18px !important;
}

/* Login popover panel sizing + font */
div[data-testid="stPopover"] div[role="dialog"] {
    min-width: 320px !important;
    max-width: 360px !important;
    padding: 14px 16px !important;
}

.login-label {
    font-size: 14px;
}

div[data-testid="stPopover"] .stTextInput input {
    height: 40px !important;
    font-size: 16px !important;
}

div[data-testid="stPopover"] .stButton > button {
    font-size: 18px !important;
    padding: 10px 18px !important;
}

/* Horizontal navigation buttons (scoped to Navigation) */
div[role="radiogroup"][aria-label="Navigation"] label {
    font-size: 140px !important;    /* increase font size */
    font-weight: 700 !important;    /* slightly bolder */
    color: #0b3d91 !important;      /* dark blue */
    cursor: pointer;                /* hand icon */
    padding: 12px 20px !important;  /* increase clickable area */
    min-height: 90px !important;    /* taller click target */
    display: inline-flex !important;
    align-items: center !important;
    margin-right: 100px !important;
}

/* Streamlit 1.53.0: actual text is inside nested elements */
div[role="radiogroup"][aria-label="Navigation"] label p,
div[role="radiogroup"][aria-label="Navigation"] label span,
div[role="radiogroup"][aria-label="Navigation"] label * {
    font-size: 30px !important;
    font-weight: 700 !important;
    color: #0b3d91 !important;
}

/* Hover effect */
div[role="radiogroup"][aria-label="Navigation"] label:hover {
    color: #4da3ff !important;     /* highlight on hover */
}

/* Review Fraud > Action radio smaller */
div[role="radiogroup"][aria-label="Action"] label,
div[role="radiogroup"][aria-label="Action"] label p,
div[role="radiogroup"][aria-label="Action"] label span,
div[role="radiogroup"][aria-label="Action"] label * {
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* INPUT */
input {
    height:42px!important;
    border-radius:8px!important;
}

/* BUTTON */
.stButton>button {
    background:#0b5ed7;
    color:white;
    border-radius:20px;
    border:none;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:#0f2a44;
}

section[data-testid="stSidebar"] * {
    color:white;
}

/* METRIC */
[data-testid="metric-container"] {
    background:white;
    padding:18px;
    border-radius:14px;
    box-shadow:0 4px 12px rgba(0,0,0,.1);
}

</style>
""", unsafe_allow_html=True)

# ================= CONFIG =================
BANK_NAME = "ABC National Bank"
MODEL_PATH = "fraud_xgb_pipeline.pkl"
TRANSACTION_CSV = "transactions.csv"
AUDIT_CSV = "fraud_audit_log.csv"

model = joblib.load(MODEL_PATH)

# ================= BANKERS =================
BANKERS = {
    "B001": {"name": "Josam", "password": "admin123", "role": "Fraud Analyst"},
    "B002": {"name": "Alex", "password": "bank123", "role": "Senior Officer"},
}

# ================= SESSION =================
for k in ["logged_in","emp_id","emp_name","role"]:
    if k not in st.session_state:
        st.session_state[k] = ""

# ================= HEADER =================

# ================= HEADER =================

st.markdown(
    f'''
    <div class="bank-header">
        <div class="header-contact header-ticker">
            <span class="header-ticker-text">
                <span class="header-block">
                    <span class="bank-name">
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 3L2 8v2h20V8L12 3zm-8 9h2v7H4v-7zm4 0h2v7H8v-7zm4 0h2v7h-2v-7zm4 0h2v7h-2v-7zM2 21h20v-2H2v2z"/>
                        </svg>
                        {BANK_NAME}
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/>
                        </svg>
                        Address: 2/78G, Arinalur, Chennai
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M6.6 2.6c.4-.4 1-.5 1.5-.2l3.1 1.7c.6.3.8 1 .5 1.6l-1.2 2.3a1 1 0 0 0 .1 1.1l3.4 3.4a1 1 0 0 0 1.1.1l2.3-1.2c.6-.3 1.3-.1 1.6.5l1.7 3.1c.3.5.2 1.2-.2 1.5l-1.7 1.7c-1.2 1.2-3 1.7-4.7 1.2-3-1-6-3-8.5-5.5S2.2 9.5 1.2 6.5c-.5-1.7 0-3.5 1.2-4.7l1.7-1.7z"/>
                        </svg>
                        Phone: 9876543021
                    </span>
                </span>
                <span class="header-block">
                    <span class="bank-name">
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 3L2 8v2h20V8L12 3zm-8 9h2v7H4v-7zm4 0h2v7H8v-7zm4 0h2v7h-2v-7zm4 0h2v7h-2v-7zM2 21h20v-2H2v2z"/>
                        </svg>
                        {BANK_NAME}
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/>
                        </svg>
                        Address: 2/78G, Arinalur, Chennai
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M6.6 2.6c.4-.4 1-.5 1.5-.2l3.1 1.7c.6.3.8 1 .5 1.6l-1.2 2.3a1 1 0 0 0 .1 1.1l3.4 3.4a1 1 0 0 0 1.1.1l2.3-1.2c.6-.3 1.3-.1 1.6.5l1.7 3.1c.3.5.2 1.2-.2 1.5l-1.7 1.7c-1.2 1.2-3 1.7-4.7 1.2-3-1-6-3-8.5-5.5S2.2 9.5 1.2 6.5c-.5-1.7 0-3.5 1.2-4.7l1.7-1.7z"/>
                        </svg>
                        Phone: 9876543021
                    </span>
                </span>
                <span class="header-block">
                    <span class="bank-name">
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 3L2 8v2h20V8L12 3zm-8 9h2v7H4v-7zm4 0h2v7H8v-7zm4 0h2v7h-2v-7zm4 0h2v7h-2v-7zM2 21h20v-2H2v2z"/>
                        </svg>
                        {BANK_NAME}
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/>
                        </svg>
                        Address: 2/78G, Arinalur, Chennai
                    </span>
                    &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;
                    <span>
                        <svg class="header-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M6.6 2.6c.4-.4 1-.5 1.5-.2l3.1 1.7c.6.3.8 1 .5 1.6l-1.2 2.3a1 1 0 0 0 .1 1.1l3.4 3.4a1 1 0 0 0 1.1.1l2.3-1.2c.6-.3 1.3-.1 1.6.5l1.7 3.1c.3.5.2 1.2-.2 1.5l-1.7 1.7c-1.2 1.2-3 1.7-4.7 1.2-3-1-6-3-8.5-5.5S2.2 9.5 1.2 6.5c-.5-1.7 0-3.5 1.2-4.7l1.7-1.7z"/>
                        </svg>
                        Phone: 9876543021
                    </span>
                </span>
            </span>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

c1, c2 = st.columns([5, 2])

with c1:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:flex-start;gap:5px;">
        <div style="display:flex;align-items:center;gap:15px;">
            <img src="https://cdn-icons-png.flaticon.com/512/483/483947.png" width="75">
            <div style="display:flex; flex-direction:column; gap:0px;">
                <span style="font-size:46px; font-weight:900; color:#0b3d91;">
                    {BANK_NAME}
                </span>
                <span style="font-size:46px; font-weight:900; color:#0b3d91;">
                    एबीसी नेशनल बैंक
                </span>
            </div>
        </div>
        <!-- Subtitle below the bank name -->
        <span style="font-size:30px; font-weight:500; color:#7ec0ee; margin-left:75px;">
            Welcome to Fraud Detection System
        </span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if not st.session_state.logged_in:
        st.markdown('<div class="login-popover-wrap">', unsafe_allow_html=True)
        with st.popover("🔐 Login"):
            st.markdown('<div class="login-label">Employee ID</div>', unsafe_allow_html=True)
            emp = st.text_input("", key="login_emp_id", label_visibility="collapsed")

            st.markdown('<div class="login-label">Password</div>', unsafe_allow_html=True)
            pwd = st.text_input("", type="password", key="login_pwd", label_visibility="collapsed")

            if st.button("Login", key="login_btn"):
                if emp in BANKERS and BANKERS[emp]["password"] == pwd:
                    st.session_state.logged_in = True
                    st.session_state.emp_id = emp
                    st.session_state.emp_name = BANKERS[emp]["name"]
                    st.session_state.role = BANKERS[emp]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Show logged-in employee info
        st.markdown(f"""
        <div class="login-status">
            <div class="login-status-title">Logged in: {st.session_state.emp_name}</div>
            <div class="login-status-role">{st.session_state.role}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="logout-spacer"></div>', unsafe_allow_html=True)
        logout_col1, logout_col2, logout_col3 = st.columns([1, 1, 1])
        with logout_col2:
            if st.button("Logout", key="logout_btn"):
                st.session_state.clear()
                st.rerun()



st.markdown("</div>", unsafe_allow_html=True)

# ==============================================

# Reduce spacing above Streamlit radio buttons
st.markdown("""
<style>
/* Bring navigation closer to bank header */
.css-1r6slb0s {  /* Streamlit radio container class */
    margin-top: -70px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= NAV =================
nav_options = ["📊 Dashboard","🛡 Fraud Detection","🚨 Review Fraud","📝 Audit Logs"]

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🚨 Review Fraud"

page = st.radio(
    "Navigation",
    nav_options,
    horizontal=True,
    key="nav_page",
    label_visibility="collapsed",
)

# ================= PAGE SUBTITLE =================

page_subtitle = ""
if page == "📊 Dashboard":
    page_subtitle = "Dashboard – Monitor Transactions"
elif page == "🛡 Fraud Detection":
    page_subtitle = "Welcome to Fraud Analytics"
elif page == "🚨 Review Fraud":
    page_subtitle = "Review Pending Fraud Transactions"
elif page == "📝 Audit Logs":
    page_subtitle = "Audit Logs Overview"

# ================= CENTERED SUBTITLE =================
st.markdown(f"""
<div style="text-align:center; margin-top:10px; margin-bottom:20px;">
    <span style="font-size:22px; font-weight:500; color:#4da3ff;">
        {page_subtitle}
    </span>
</div>
""", unsafe_allow_html=True)

# ================= LOGIN GATE =================
if not st.session_state.logged_in:
    st.info("Please login to continue")
    st.stop()


# ================= CSV =================
TRANSACTION_COLUMNS=["txn_id","transaction_type","amount","fraud_score","final_decision","checked_by","timestamp"]
AUDIT_COLUMNS=["txn_id","banker_id","banker_name","role","action","remarks","action_time"]

def log_transaction(d):
    pd.DataFrame([[d[c] for c in TRANSACTION_COLUMNS]],columns=TRANSACTION_COLUMNS)\
        .to_csv(TRANSACTION_CSV,mode="a",header=not os.path.exists(TRANSACTION_CSV),index=False)

def log_audit(d):
    pd.DataFrame([[d[c] for c in AUDIT_COLUMNS]],columns=AUDIT_COLUMNS)\
        .to_csv(AUDIT_CSV,mode="a",header=not os.path.exists(AUDIT_CSV),index=False)

# ================= BANK DECISION =================
def bank_decision(fraud_prob,amount,txn_type,newbalanceOrig):

    if amount > 500000:
        return "❌ BLOCKED","Daily limit exceeded"

    if amount > 200000:
        return "⏳ REVIEW","High value transaction"

    if newbalanceOrig == 0:
        return "⏳ REVIEW","Sender balance zero"

    if fraud_prob < 0.30:
        return "✅ APPROVED","Low risk"

    elif fraud_prob < 0.70:
        return "⏳ REVIEW","Medium risk"

    else:
        return "❌ BLOCKED","High fraud probability"

# ================= PAGES =================

def dashboard():
    st.subheader("📊 Dashboard")

    if not os.path.exists(TRANSACTION_CSV):
        st.info("No transactions yet")
        return

    df = pd.read_csv(TRANSACTION_CSV)

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Checked",len(df))
    c2.metric("Blocked",df["final_decision"].str.contains("BLOCKED").sum())
    c3.metric("Under Review",df["final_decision"].str.contains("REVIEW").sum())

def fraud_detection():

    st.subheader("🛡 Fraud Detection")

    with st.form("txn"):
        txn_type = st.selectbox("Transaction Type",["PAYMENT","TRANSFER","CASH_OUT","DEPOSIT"])
        amount = st.number_input("Amount",0.0)
        oldbal_org = st.number_input("Sender Balance",0.0)
        oldbal_dest = st.number_input("Receiver Balance",0.0)
        submit = st.form_submit_button("Run Check")

    if not submit:
        return

    newbal_org = max(oldbal_org-amount,0)
    newbal_dest = oldbal_dest+amount

    fraud_prob = model.predict_proba(pd.DataFrame([{
        "type":txn_type,
        "amount":amount,
        "oldbalanceOrg":oldbal_org,
        "newbalanceOrig":newbal_org,
        "oldbalanceDest":oldbal_dest,
        "newbalanceDest":newbal_dest
    }]))[0][1]

    decision,reason = bank_decision(fraud_prob,amount,txn_type,newbal_org)

    st.success(f"{decision} — Fraud Score {fraud_prob*100:.2f}%")

    tid = str(uuid.uuid4())[:8]

    log_transaction({
        "txn_id":tid,
        "transaction_type":txn_type,
        "amount":amount,
        "fraud_score":fraud_prob,
        "final_decision":decision,
        "checked_by":st.session_state.emp_name,
        "timestamp":datetime.now().isoformat()
    })

    # Audit log is recorded only when a banker reviews/acts on a case

def review_transactions():

    st.subheader("🚨 Review Fraud")

    if not os.path.exists(TRANSACTION_CSV):
        st.info("No data")
        return

    df = pd.read_csv(TRANSACTION_CSV)

    flagged = df[df["final_decision"].str.contains("REVIEW|BLOCKED")]

    if flagged.empty:
        st.success("No pending cases")
        return

    txn = st.selectbox("Transaction ID",flagged["txn_id"])
    action = st.radio("Action",["Confirm Fraud","Mark Legit","Escalate"])
    remarks = st.text_area("Remarks")

    if st.button("Submit"):
        log_audit({
            "txn_id":txn,
            "banker_id":st.session_state.emp_id,
            "banker_name":st.session_state.emp_name,
            "role":st.session_state.role,
            "action":action,
            "remarks":remarks,
            "action_time":datetime.now().isoformat()
        })
        st.success("Recorded")


def audit_logs():

    st.subheader("📝 Audit Logs")

    if os.path.exists(AUDIT_CSV):
        st.dataframe(pd.read_csv(AUDIT_CSV),use_container_width=True)
    else:	
        st.info("No audit logs")

# ================= ROUTER =================
if page=="📊 Dashboard": dashboard()
elif page=="🛡 Fraud Detection": fraud_detection()
elif page=="🚨 Review Fraud": review_transactions()
elif page=="📝 Audit Logs": audit_logs()

