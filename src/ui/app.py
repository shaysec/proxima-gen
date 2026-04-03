import sys
import os

# --- PATH FIXING ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from langchain_core.messages import HumanMessage
from src.agent.agent import agent_executor

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SQLITE_DB_PATH = os.path.join(BASE_DIR, 'data', 'ai_vulnerabilities.db')

st.set_page_config(page_title="AI Security Sentinel", page_icon="🛡️", layout="wide")

# --- HELPER FUNCTIONS ---
def get_db_data():
    if os.path.exists(SQLITE_DB_PATH):
        conn = sqlite3.connect(SQLITE_DB_PATH)
        df = pd.read_sql_query("SELECT * FROM vulnerabilities", conn)
        conn.close()
        return df
    return pd.DataFrame()

# --- SIDEBAR ---
st.sidebar.title("🛡️ AI Security Hub")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Executive Dashboard", "Investigative Chat"])
st.sidebar.markdown("---")

# --- PAGE 1: EXECUTIVE DASHBOARD ---
if page == "Executive Dashboard":
    st.title("📊 AI Vulnerability Intelligence Report")
    st.markdown("Comprehensive view of all discovered threats across monitored frameworks.")

    df = get_db_data()

    if not df.empty:
        # 1. Filters Row
        st.markdown("### 🔍 Filters")
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            framework_filter = st.multiselect("Framework", options=df['framework'].unique(), default=df['framework'].unique())
        with col_f2:
            severity_filter = st.multiselect("Severity", options=df['severity'].unique(), default=df['severity'].unique())
        with col_f3:
            search_query = st.text_input("Search Description", "")

        # Apply Filters
        mask = (df['framework'].isin(framework_filter)) & \
               (df['severity'].isin(severity_filter)) & \
               (df['description'].str.contains(search_query, case=False))
        filtered_df = df[mask]

        # 2. Key Metrics
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Threats", len(filtered_df))
        m2.metric("Critical Assets", len(filtered_df[filtered_df['severity'] == 'High']))
        m3.metric("Frameworks", len(filtered_df['framework'].unique()))
        m4.metric("Last Scan", filtered_df['discovery_date'].max() if not filtered_df.empty else "N/A")

        # 3. Visual Analytics
        st.markdown("---")
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Threat Distribution by Category")
            st.bar_chart(filtered_df['category'].value_counts())
        with c2:
            st.subheader("Framework Coverage")
            st.pie_chart(filtered_df['framework'].value_counts())

        # 4. Data Table & Export
        st.markdown("---")
        st.subheader("Detailed Vulnerability Log")
        st.dataframe(filtered_df.sort_values(by="discovery_date", ascending=False), use_container_width=True)
        
        # Export Button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Report to CSV",
            data=csv,
            file_name=f"ai_security_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
    else:
        st.info("The intelligence database is currently empty. Please run the Daily Scanner or use the Chat to populate data.")

# --- PAGE 2: INVESTIGATIVE CHAT ---
elif page == "Investigative Chat":
    st.title("🕵️ Investigative AI Agent")
    st.markdown("Deep-dive into specific threats. All findings are automatically persisted to the dashboard.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Command the agent..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing threat intelligence..."):
                try:
                    inputs = {"messages": [HumanMessage(content=prompt)]}
                    result = agent_executor.invoke(inputs)
                    response = result["messages"][-1].content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    if "Successfully" in response:
                        st.toast("Intelligence Updated!", icon="🛡️")
                except Exception as e:
                    st.error(f"Agent Error: {e}")