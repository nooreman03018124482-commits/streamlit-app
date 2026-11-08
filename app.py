import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Vigilaire - Cybersecurity SaaS",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for Professional Red Branding on Dark Background
st.markdown("""
    <style>
    .brand-title {
        color: #FF4B4B;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0px;
        line-height: 1.2;
    }
    .brand-tagline {
        color: #FF6B6B;
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Bilingual Dictionary / لغت (English & Urdu)
translations = {
    "English": {
        "brand_title": "Vigilaire",
        "brand_subtitle": "Continuous Intelligence. Real-Time Protection.",
        "nav_title": "Control Panel",
        "nav_overview": "Platform Overview",
        "nav_scan": "Automated Security Check",
        "nav_threat": "Threat Intelligence Feed",
        "nav_block": "Active Blocking Engine",
        "nav_plans": "Enterprise & Subscription Plans",
        
        "hero_heading": "Autonomous Cyber Security for Modern Web Assets",
        "hero_desc": "Vigilaire delivers continuous vulnerability monitoring, threat matching, and automated threat suppression for websites, web applications, online stores, and database endpoints.",
        
        "card1_title": "Continuous Vulnerability Discovery",
        "card1_desc": "Automated daily discovery of misconfigurations, outdated components, and publicly exposed database endpoints.",
        
        "card2_title": "Plain-Language Intelligence",
        "card2_desc": "Instant alerts with prioritized severity rankings and step-by-step remediation fix guides in simple English and Urdu.",
        
        "card3_title": "Automated Threat Suppression",
        "card3_desc": "Blocks brute-force credential spraying and high-confidence attack vectors in real time while root fixes are applied.",
        
        "exec_dash": "Executive Performance Dashboard",
        "metric_assets": "Monitored Assets",
        "metric_latency": "Threat Detection Latency",
        "metric_false": "False Positive Target",
        "metric_uptime": "System Uptime",
        
        "scan_heading": "Instant Security Endpoint Inspection",
        "scan_desc": "Conduct an immediate automated vulnerability inspection on target web infrastructure.",
        "scan_input": "Target Endpoint URL",
        "scan_btn": "Initiate Security Audit 🚀",
        
        "pricing_heading": "Flexible Security Tiering",
        "pricing_desc": "Transparent pricing tailored for every digital scale.",
        "plan_starter": "Starter",
        "price_starter": "PKR 5,999 / mo",
        "feat_1": "1 Web Asset",
        "feat_2": "Weekly Vulnerability Discovery",
        "feat_3": "Email Remediation Alerts",
        "feat_4": "Basic Credential Guard",
        "btn_starter": "Deploy Starter"
    },
    "اردو": {
        "brand_title": "ویجیلاائر (Vigilaire)",
        "brand_subtitle": "مسلسل ذہانت۔ ریئل ٹائم تحفظ۔",
        "nav_title": "کنٹرول پینل",
        "nav_overview": "پلیٹ فارم کا جائزہ",
        "nav_scan": "خودکار سیکیورٹی چیک",
        "nav_threat": "تھ্রেট انٹیلی جنس فیڈ",
        "nav_block": "ایکٹیভ بلاکنگ انجن",
        "nav_plans": "انٹرپرائز اور سبسکرپشن پلانز",
        
        "hero_heading": "جدید ویب اثاثوں کے لیے خودکار سائبر سیکیورٹی",
        "hero_desc": "ویجیلاائر ویب سائٹس، ویب ایپلیکیشنز، آن لائن سٹورز اور ڈیٹا بیس کے لیے مسلسل کمزوری کی نگرانی اور خودکار خطرات سے دفاع فراہم کرتا ہے۔",
        
        "card1_title": "مسلسل کمزوری کی دریافت",
        "card1_desc": "غلط کنفیگریشنز، پرانے سسٹمز اور پبلک ڈیٹا بیس اینڈ پوائنٹس کی روزانہ خودکار دریافت۔",
        
        "card2_title": "آسان زبان میں انٹیلی جنس",
        "card2_desc": "آسان انگریزی اور اردو میں فوری الرٹس اور قدم بہ قدم حل کی رہنمائی۔",
        
        "card3_title": "خودکار خطرات کی روک تھام",
        "card3_desc": "حملوں کو ریئل ٹائم میں روکنا جبکہ اندرونی مسائل کو حل کیا جاتا ہے۔",
        
        "exec_dash": "ایگزیکٹو پرفارمنس ڈ্যাশবোর্ড",
        "metric_assets": "زیرِ نگرانی اثاثے",
        "metric_latency": "خطرے کا پتہ لگانے کی رفتار",
        "metric_false": "فالس پازیٹیو ہدف",
        "metric_uptime": "سسٹم کا وقتِ کار (Uptime)",
        
        "scan_heading": "فوری سیکیورٹی اینڈ پوائنٹ معائنہ",
        "scan_desc": "ہدف ویب انفراسٹرکچر پر فوری خودکار سیکیورٹی معائنہ کریں۔",
        "scan_input": "ہدف اینڈ پوائنٹ یو آر ایل",
        "scan_btn": "سیکیورٹی آڈٹ شروع کریں 🚀",
        
        "pricing_heading": "لچکدار سیکیورٹی ٹیرف",
        "pricing_desc": "ہر ڈیجیٹل پیمانے کے لیے موزوں شفاف قیمتیں۔",
        "plan_starter": "اسٹارٹر",
        "price_starter": "PKR 5,999 / ماہ",
        "feat_1": "1 ویب اثاثہ",
        "feat_2": "ہفتہ وار کمزوری کی دریافت",
        "feat_3": "ای میل کے ذریعے اصلاحی الرٹس",
        "feat_4": "بنیادی کریڈینشل گارڈ",
        "btn_starter": "اسٹارٹر منتخب کریں"
    }
}

# Sidebar Language Selection
st.sidebar.title("🌍 Language / زبان")
selected_lang = st.sidebar.selectbox("Choose Language", ["English", "اردو"])
t = translations[selected_lang]

# Navigation
st.sidebar.markdown("---")
st.sidebar.subheader(t["nav_title"])
nav_selection = st.sidebar.radio(
    "Navigation", 
    [t["nav_overview"], t["nav_scan"], t["nav_threat"], t["nav_block"], t["nav_plans"]]
)

# Main Dashboard Header with Professional Red Styling
st.markdown(f'<p class="brand-title">🛡️ {t["brand_title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="brand-tagline">{t["brand_subtitle"]}</p>', unsafe_allow_html=True)
st.markdown("---")

if nav_selection == t["nav_overview"]:
    st.header(t["hero_heading"])
    st.write(t["hero_desc"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**{t['card1_title']}**\n\n{t['card1_desc']}")
    with col2:
        st.info(f"**{t['card2_title']}**\n\n{t['card2_desc']}")
    with col3:
        st.info(f"**{t['card3_title']}**\n\n{t['card3_desc']}")
        
    st.markdown("---")
    st.subheader(t["exec_dash"])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t["metric_assets"], "150 Active", "+8.5% this month")
    m2.metric(t["metric_latency"], "< 5 mins", "-12% optimized")
    m3.metric(t["metric_false"], "< 2.0%", "Strict tuning")
    m4.metric(t["metric_uptime"], "99.99%", "Stable")

elif nav_selection == t["nav_scan"]:
    st.header(t["scan_heading"])
    st.write(t["scan_desc"])
    target_url = st.text_input(t["scan_input"], "https://example.com")
    if st.button(t["scan_btn"]):
        st.success("✨ Security audit initiated successfully across target vectors.")

elif nav_selection == t["nav_plans"]:
    st.header(t["pricing_heading"])
    st.write(t["pricing_desc"])
    
    st.subheader(t["plan_starter"])
    st.markdown(f"## **{t['price_starter']}**")
    st.markdown(f"- {t['feat_1']}")
    st.markdown(f"- {t['feat_2']}")
    st.markdown(f"- {t['feat_3']}")
    st.markdown(f"- {t['feat_4']}")
    st.button(t["btn_starter"])

else:
    st.header(nav_selection)
    st.write("Module active and operational.")