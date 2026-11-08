# app.py
from database import get_cisa_kev_threats, log_audit_record
from scanner import run_security_scan
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Vigilaire | Always-On Cyber Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling (CSS)
st.markdown(
    """
    <style>
    .main { background-color: #F9FAFB; }
    .brand-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 0px;
    }
    .brand-tagline {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2563EB;
        margin-top: 4px;
        margin-bottom: 25px;
    }
    .feature-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    .feature-card h3 {
        color: #1E293B;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: #64748B;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .badge-active {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    '<div class="brand-header">🛡️ Vigilaire</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="brand-tagline">Continuous Intelligence. Real-Time Protection.</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Sidebar Navigation
st.sidebar.markdown("### 🎛️ Control Panel")
app_mode = st.sidebar.radio(
    "Navigation",
    [
        "Platform Overview",
        "🔍 Automated Security Check",
        "📊 Threat Intelligence Feed",
        "🛑 Active Blocking Engine",
        "💼 Enterprise & Subscription Plans",
    ],
)

# ---------------------------------------------------------
# 1. PLATFORM OVERVIEW
# ---------------------------------------------------------
if app_mode == "Platform Overview":
  st.markdown("### Autonomous Cyber Security for Modern Web Assets")
  st.write(
      "Vigilaire delivers continuous vulnerability monitoring, threat"
      " matching, and automated threat suppression for websites, web"
      " applications, online stores, and database endpoints[span_0](start_span)[span_0](end_span)."
  )

  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns(3)

  with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🔍 Continuous Vulnerability Discovery</h3>
            <p>Automated daily discovery of misconfigurations, outdated components, and publicly exposed database endpoints[span_1](start_span)[span_1](end_span).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📢 Plain-Language Intelligence</h3>
            <p>Instant alerts with prioritized severity rankings and step-by-step remediation fix guides in simple English and Urdu[span_2](start_span)[span_2](end_span).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🛡️ Automated Threat Suppression</h3>
            <p>Blocks brute-force credential spraying and high-confidence attack vectors in real time while root fixes are applied[span_3](start_span)[span_3](end_span).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br><br>", unsafe_allow_html=True)
  st.markdown("### Executive Performance Dashboard")
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Monitored Assets", "150 Active", "+12 this week")
  m2.metric("Threat Detection Latency", "< 5 mins", "Real-time pipeline")
  m3.metric("False Positive Target", "< 2.0%", "Strict tuning")
  m4.metric("System Uptime", "99.99%", "Fail-open architecture")

# ---------------------------------------------------------
# 2. AUTOMATED SECURITY CHECK
# ---------------------------------------------------------
elif app_mode == "🔍 Automated Security Check":
  st.markdown("### Instant Security Endpoint Inspection")
  st.write(
      "Conduct an immediate automated vulnerability inspection on target web"
      " infrastructure[span_4](start_span)[span_4](end_span)."
  )

  c1, c2 = st.columns([3, 1])
  with c1:
    target_url = st.text_input(
        "Target Endpoint URL", placeholder="https://example.com"
    )
  with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_button = st.button("Initiate Security Audit 🚀", type="primary")

  if scan_button:
    if not target_url:
      st.warning("Please specify a target URL.")
    else:
      with st.spinner("Analyzing web application headers and attack patterns..."):
        result = run_security_scan(target_url)

        if result["status"] == "success":
          st.success("Security Inspection Completed Successfully")

          res_col1, res_col2 = st.columns(2)
          res_col1.metric("Response Time", f"{result['elapsed_time']} seconds")
          res_col2.metric("Discovered Findings", len(result["issues"]))

          st.markdown("#### Audit Findings & Remediation Steps")
          for issue in result["issues"]:
            if issue["level"] == "Critical":
              st.error(f"🔴 **{issue['title']}** (Severity: Critical)")
            else:
              st.info(f"🟢 **{issue['title']}** (Status: Passed)")

            st.write(f"**Impact Summary:** {issue['why']}")
            st.markdown(f"**Remediation Guide:**\n{issue['fix']}")

          log_audit_record(target_url, "Medium")
        else:
          st.error(
              f"Scan Execution Failed. Target unreachable: {result['message']}"
          )

# ---------------------------------------------------------
# 3. THREAT INTELLIGENCE FEED
# ---------------------------------------------------------
elif app_mode == "📊 Threat Intelligence Feed":
  st.markdown("### Synchronized Global Vulnerability Repository")
  st.write(
      "Real-time ingestion pipeline matching assets against CISA KEV, NVD, and"
      " CVE catalogs."
  )

  st.markdown(
      '<span class="badge-active">● PIPELINE ONLINE</span>',
      unsafe_allow_html=True,
  )
  st.markdown("<br>", unsafe_allow_html=True)

  threats = get_cisa_kev_threats()
  st.table(threats)

# ---------------------------------------------------------
# 4. ACTIVE BLOCKING ENGINE
# ---------------------------------------------------------
elif app_mode == "🛑 Active Blocking Engine":
  st.markdown("### Real-Time Protection & Policy Enforcement")
  st.write(
      "Configure automated inline threat suppression and access policy modes"
      "."
  )

  mode = st.select_slider(
      "Enforcement Policy Level:",
      options=["Alert-only", "Standard Protection", "Strict Enforcement"],
      value="Standard Protection",
  )

  if mode == "Alert-only":
    st.info(
        "ℹ️ **Alert-only:** Telemetry monitored and logged. Threat alerts sent"
        " to system owners without automated blocking."
    )
  elif mode == "Standard Protection":
    st.success(
        "🛡️ **Standard Protection (Recommended):** Automatically throttles"
        " suspicious database command structures and locks brute-force login"
        " patterns."
    )
  else:
    st.warning(
        "⚡ **Strict Enforcement:** Aggressive protection matrix blocking both"
        " medium and high-confidence threat signatures."
    )

# ---------------------------------------------------------
# 5. SUBSCRIPTION PLANS
# ---------------------------------------------------------
elif app_mode == "💼 Enterprise & Subscription Plans":
  st.markdown("### Flexible Security Tiering")
  st.write("Transparent pricing tailored for every digital scale[span_5](start_span)[span_5](end_span).")

  pcol1, pcol2, pcol3 = st.columns(3)

  with pcol1:
    st.markdown("### Starter")
    st.markdown("## PKR 5,999 / mo")
    st.write("• **1 Web Asset**")
    st.write("• Weekly Vulnerability Discovery")
    st.write("• Email Remediation Alerts")
    st.write("• Basic Credential Guard")
    st.button("Deploy Starter", key="sub1", use_container_width=True)

  with pcol2:
    st.markdown("### Growth")
    st.markdown("## PKR 17,999 / mo")
    st.write("• **Up to 5 Assets**")
    st.write("• Daily Continuous Scans")
    st.write("• Full Query Injection Blocking")
    st.write("• Executive Monthly Reports")
    st.button(
        "Deploy Growth", key="sub2", type="primary", use_container_width=True
    )

  with pcol3:
    st.markdown("### Business")
    st.markdown("## PKR 49,999 / mo")
    st.write("• **Up to 20 Assets**")
    st.write("• Real-Time Threat Suppression")
    st.write("• Instant WhatsApp & Slack Alerts")
    st.write("• Virtual Patching Engine")
    st.button("Deploy Business", key="sub3", use_container_width=True)