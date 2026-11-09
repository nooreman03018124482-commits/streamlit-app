import hashlib
import re
import time

import streamlit as st

# ----------------------------------------------------------------------------
# Page configuration
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Vigilaire | Continuous Security. Continuous Protection.",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def h(s: str) -> str:
    """Flatten HTML so Markdown never treats indented lines as code blocks."""
    return "".join(line.strip() for line in s.strip().splitlines())


# ----------------------------------------------------------------------------
# Content (English and Urdu), based on the Vigilaire Business Plan 2026
# ----------------------------------------------------------------------------
T = {
    "English": {
        "dir": "ltr",
        "tagline": "Continuous Security. Continuous Protection.",
        "lang_label": "Language",
        "nav": {
            "overview": "Overview",
            "scan": "Free Security Check",
            "threat": "Threat Feed",
            "block": "Blocking Engine",
            "plans": "Pricing",
        },
        "hero_title": "The watchdog that never sleeps for your website.",
        "hero_sub": "Vigilaire checks your website and databases every day, warns you in simple Urdu and English with a step-by-step fix guide, and blocks the attacks it can safely stop.",
        "hero_cta1": "Run a free security check",
        "hero_cta2": "See pricing",
        "stats": [
            ("< 5 min", "Target time from detection to owner alert"),
            ("< 2%", "Target false-block rate"),
            ("Urdu + English", "Alerts, fix guides and support"),
            ("PKR 5,999", "Starting price per month"),
        ],
        "three_title": "Find it. Warn you. Block it.",
        "three_sub": "Three jobs in one service, built for businesses without a security team.",
        "cards": [
            ("🔍", "Find weak spots", "Continuous scanning of your website and internet-facing database endpoints for misconfigurations, outdated components and newly published CVEs."),
            ("💬", "Warn you in plain language", "Every alert says what is wrong, why it matters and how to fix it, ranked from most to least dangerous. Sent by email, WhatsApp or Slack."),
            ("🛑", "Block what is safe to block", "With your written permission, Vigilaire stops password guessing and high-confidence malicious requests while your permanent fix is prepared."),
        ],
        "how_title": "How Vigilaire works",
        "how_sub": "The same cycle runs every day for every authorized website.",
        "steps": [
            ("Sign up and prove ownership", "Add your site, verify it with a DNS record or meta tag, and sign the written authorization."),
            ("Discover assets", "We map your public pages, login forms and database ports."),
            ("Test against attack patterns", "Assets are checked against known attacks, misconfigurations and new CVEs."),
            ("Rank by severity", "Findings are ordered from most to least dangerous."),
            ("Alert within minutes", "You get a short warning and a fix guide by email or WhatsApp."),
            ("Protect and re-test", "Blocking runs in your chosen mode, and we re-test after you fix."),
        ],
        "who_title": "Built for businesses that run a website but have no security team",
        "who": ["Online stores", "Software companies and start-ups", "Payment and wallet firms", "Clinics and hospitals", "Schools and universities", "Hotels and tour operators", "Web agencies (resellers)"],
        "cmp_title": "Why not an enterprise tool or a free scanner?",
        "cmp_head": ["", "Enterprise tools", "Free scanners", "Vigilaire"],
        "cmp_rows": [
            ("Price", "Dollar pricing", "Free", "Rupee pricing from PKR 5,999"),
            ("Needs a trained operator", "Yes", "Yes", "No"),
            ("Alerts in plain language", "Rarely", "No", "Urdu and English"),
            ("Blocks attacks", "Sold separately", "No", "Built in, with your permission"),
            ("Local support", "No", "No", "Urdu and English, Pakistan hours"),
        ],
        "kpi_title": "Year-1 service targets",
        "kpi_note": "These are planning targets from the Vigilaire Business Plan 2026, not live measurements.",
        "kpis": [
            ("Customers by Month 12", "150", "Target"),
            ("Detection to alert", "< 5 min", "Target"),
            ("False-alert rate", "7%", "By Month 12"),
            ("Monthly churn", "< 4%", "Target"),
        ],
        "scan_title": "Free security check",
        "scan_sub": "Enter your website address to see the kind of report Vigilaire produces. This page runs a demonstration only. A real scan needs proof of ownership and a signed authorization.",
        "scan_input": "Website address",
        "scan_btn": "Run demo check",
        "scan_bad": "Please enter a valid website address, for example https://shop.example.pk",
        "scan_progress": ["Verifying address format...", "Mapping public pages and login forms...", "Matching against known weaknesses...", "Ranking findings by severity..."],
        "scan_done": "Demo check finished for",
        "scan_demo_note": "Demonstration data only. No request was sent to your website. Sign up to run an authorized scan.",
        "sev": {"Critical": "Critical", "High": "High", "Medium": "Medium"},
        "fix_label": "How to fix it",
        "why_label": "Why it matters",
        "threat_title": "Threat intelligence feed",
        "threat_sub": "Vigilaire pulls new entries every day from CISA KEV, NVD and CVE.org, matches them to each customer's software list and scores them.",
        "threat_src": [
            ("CISA KEV", "Weaknesses already used in real attacks", "Highest-priority alerts"),
            ("NVD", "Details, affected products and CVSS severity score", "Matching and scoring"),
            ("CVE.org", "Official identifiers and short descriptions", "Reference and cross-check"),
        ],
        "threat_head": ["CVE", "Severity", "Summary", "Vigilaire action"],
        "threat_rows": [
            ("CVE-2023-34362", "Critical", "SQL injection in file-transfer software, exploited at scale in 2023 (MOVEit).", "Owner alerted; virtual patch rule available"),
            ("CVE-2026-4891", "Critical", "Remote code execution in a legacy database driver.", "Owner alerted with fix guide"),
            ("CVE-2026-3102", "High", "Cross-site scripting through weak input validation.", "Alert sent; input rule suggested"),
            ("CVE-2026-1044", "Medium", "Security header misconfiguration.", "Alert sent with one-line fix"),
        ],
        "threat_note": "Illustrative sample entries for demonstration. The live feed runs on the daily pipeline described in the business plan.",
        "block_title": "Blocking engine",
        "block_sub": "Blocking is always optional, time-limited, logged and reversible with one click. Vigilaire never tests or blocks any asset without prior written authorization.",
        "modes_title": "Choose your blocking mode",
        "modes": [
            ("Alert-only", "Finds and warns, but never blocks. Every new customer can start here."),
            ("Standard", "Blocks high-confidence attacks and repeated failed logins. The recommended default."),
            ("Strict", "Also blocks medium-confidence patterns. Safer against attacks, but more likely to affect real users."),
        ],
        "login_title": "Login protection (starting defaults)",
        "login_head": ["Condition", "Action"],
        "login_rows": [
            ("Three failed logins on one account", "Lock the account for 15 minutes and email the owner"),
            ("One IP fails on three accounts, or ten times in ten minutes", "Block the IP for 1 hour (stops password spraying)"),
            ("Attempts continue after a block", "Escalate to 24 hours, then 7 days, then manual review"),
            ("Your own office IP addresses", "Allow-listed, but still monitored"),
        ],
        "log_title": "Example interception log",
        "log_note": "Sample log for illustration. Every real block records time, rule ID, source IP and action taken.",
        "limits_title": "Honest limits",
        "limits": [
            "No service can stop every attack, such as the use of a correctly stolen password.",
            "Attackers can rotate IP addresses, so pattern-based detection is essential.",
            "Very large traffic floods (DDoS) need specialist network-level protection.",
            "If our filter is ever down, enforcement fails open so your site stays online.",
        ],
        "plans_title": "Simple pricing in rupees",
        "plans_sub": "Every plan includes blocking and a 14-day free trial. Pay annually and save 20%.",
        "per_month": "/ month",
        "popular": "Most popular",
        "plans": [
            {"name": "Starter", "price": "PKR 5,999", "usd": "about USD 21", "for": "Micro businesses with one website", "feats": ["1 website", "Weekly security checks", "Email alerts with fix guides", "Login protection (supported platforms)"], "btn": "Start free trial"},
            {"name": "Growth", "price": "PKR 17,999", "usd": "about USD 64", "for": "Small businesses with customer data online", "feats": ["Up to 5 sites or databases", "Daily security checks", "Full suspicious-query blocking", "Monthly plain-language report"], "btn": "Start free trial", "popular": True},
            {"name": "Business", "price": "PKR 49,999", "usd": "about USD 179", "for": "Firms that must show proof to clients and banks", "feats": ["Up to 20 assets", "Continuous checks", "WhatsApp alerts and safety summary", "Virtual patching and custom rules", "Priority support"], "btn": "Talk to sales"},
            {"name": "Agency", "price": "Custom", "usd": "reseller terms", "for": "Web agencies and software houses", "feats": ["Protect many client sites at once", "Commission on referred customers", "Partner dashboard and monthly statement", "Co-branded reports"], "btn": "Become a partner"},
        ],
        "extras_title": "Also available",
        "extras": [
            ("Security audit", "PKR 60,000", "One website: full scan, manual check of critical findings, written report and one re-test."),
            ("Twice-a-year audit plan", "PKR 108,000", "Two standard audits in 12 months."),
            ("Extended audit", "PKR 200,000", "Up to 5 websites or databases."),
        ],
        "toast": "Thanks. This demo site does not take sign-ups yet, but your interest is noted.",
        "cta_title": "See your risk in minutes",
        "cta_sub": "Run a free check and find out what attackers could see.",
        "footer": "Vigilaire is an entrepreneurship project of COMSATS University Islamabad, Abbottabad Campus. Prices and figures are planning estimates from the Business Plan 2026.",
    },
    "اردو": {
        "dir": "rtl",
        "tagline": "مسلسل سیکیورٹی۔ مسلسل تحفظ۔",
        "lang_label": "زبان",
        "nav": {
            "overview": "جائزہ",
            "scan": "مفت سیکیورٹی چیک",
            "threat": "خطرات کی فیڈ",
            "block": "بلاکنگ انجن",
            "plans": "قیمتیں",
        },
        "hero_title": "آپ کی ویب سائٹ کا وہ نگہبان جو کبھی نہیں سوتا۔",
        "hero_sub": "ویجیلاائر روزانہ آپ کی ویب سائٹ اور ڈیٹا بیس کو چیک کرتا ہے، آسان اردو اور انگریزی میں قدم بہ قدم حل کے ساتھ خبردار کرتا ہے، اور محفوظ طریقے سے روکے جا سکنے والے حملے روک دیتا ہے۔",
        "hero_cta1": "مفت سیکیورٹی چیک کریں",
        "hero_cta2": "قیمتیں دیکھیں",
        "stats": [
            ("< 5 منٹ", "خطرہ ملنے سے الرٹ تک کا ہدف"),
            ("< 2%", "غلط بلاک کی شرح کا ہدف"),
            ("اردو + انگریزی", "الرٹس، حل کی رہنمائی اور سپورٹ"),
            ("PKR 5,999", "ماہانہ ابتدائی قیمت"),
        ],
        "three_title": "تلاش کریں۔ خبردار کریں۔ روک دیں۔",
        "three_sub": "ایک سروس میں تین کام، ان کاروباروں کے لیے جن کے پاس سیکیورٹی ٹیم نہیں۔",
        "cards": [
            ("🔍", "کمزوریاں تلاش کرتا ہے", "آپ کی ویب سائٹ اور انٹرنیٹ پر کھلے ڈیٹا بیس اینڈ پوائنٹس میں غلط کنفیگریشن، پرانے کمپوننٹس اور نئے CVEs کی مسلسل جانچ۔"),
            ("💬", "آسان زبان میں خبردار کرتا ہے", "ہر الرٹ بتاتا ہے کہ مسئلہ کیا ہے، کیوں اہم ہے اور کیسے ٹھیک ہوگا۔ ای میل، واٹس ایپ یا سلیک پر۔"),
            ("🛑", "محفوظ حملے روکتا ہے", "آپ کی تحریری اجازت سے ویجیلاائر پاس ورڈ اندازے اور واضح بدنیتی والی درخواستیں روکتا ہے جب تک مستقل حل تیار ہو۔"),
        ],
        "how_title": "ویجیلاائر کیسے کام کرتا ہے",
        "how_sub": "یہی عمل ہر مجاز ویب سائٹ کے لیے روزانہ چلتا ہے۔",
        "steps": [
            ("سائن اپ اور ملکیت کا ثبوت", "اپنی سائٹ شامل کریں، DNS ریکارڈ یا میٹا ٹیگ سے تصدیق کریں اور تحریری اجازت نامے پر دستخط کریں۔"),
            ("اثاثوں کی نشاندہی", "ہم آپ کے پبلک صفحات، لاگ اِن فارمز اور ڈیٹا بیس پورٹس کا نقشہ بناتے ہیں۔"),
            ("حملوں کے نمونوں سے جانچ", "اثاثوں کو معلوم حملوں، غلط کنفیگریشن اور نئے CVEs کے خلاف جانچا جاتا ہے۔"),
            ("شدت کے مطابق ترتیب", "مسائل کو زیادہ سے کم خطرناک کی ترتیب میں رکھا جاتا ہے۔"),
            ("منٹوں میں الرٹ", "ای میل یا واٹس ایپ پر مختصر وارننگ اور حل کی رہنمائی ملتی ہے۔"),
            ("تحفظ اور دوبارہ جانچ", "آپ کے منتخب موڈ میں بلاکنگ چلتی ہے اور مسئلہ ٹھیک ہونے کے بعد دوبارہ جانچ ہوتی ہے۔"),
        ],
        "who_title": "ان کاروباروں کے لیے جن کی ویب سائٹ ہے مگر سیکیورٹی ٹیم نہیں",
        "who": ["آن لائن سٹورز", "سافٹ ویئر کمپنیاں اور اسٹارٹ اپس", "پیمنٹ اور والٹ کمپنیاں", "کلینک اور ہسپتال", "اسکول اور یونیورسٹیاں", "ہوٹل اور ٹور آپریٹرز", "ویب ایجنسیاں (ری سیلر)"],
        "cmp_title": "انٹرپرائز ٹول یا مفت اسکینر کیوں نہیں؟",
        "cmp_head": ["", "انٹرپرائز ٹولز", "مفت اسکینرز", "ویجیلاائر"],
        "cmp_rows": [
            ("قیمت", "ڈالر میں", "مفت", "روپوں میں، PKR 5,999 سے"),
            ("تربیت یافتہ آپریٹر درکار", "ہاں", "ہاں", "نہیں"),
            ("آسان زبان میں الرٹس", "شاذ و نادر", "نہیں", "اردو اور انگریزی"),
            ("حملے روکنا", "الگ فروخت", "نہیں", "شامل، آپ کی اجازت سے"),
            ("مقامی سپورٹ", "نہیں", "نہیں", "اردو اور انگریزی، پاکستانی اوقات"),
        ],
        "kpi_title": "پہلے سال کے سروس اہداف",
        "kpi_note": "یہ ویجیلاائر بزنس پلان 2026 کے منصوبہ بند اہداف ہیں، لائیو پیمائش نہیں۔",
        "kpis": [
            ("12ویں مہینے تک صارفین", "150", "ہدف"),
            ("خطرے سے الرٹ تک", "< 5 منٹ", "ہدف"),
            ("غلط الرٹ کی شرح", "7%", "12ویں مہینے تک"),
            ("ماہانہ چرن", "< 4%", "ہدف"),
        ],
        "scan_title": "مفت سیکیورٹی چیک",
        "scan_sub": "اپنی ویب سائٹ کا پتہ درج کریں تاکہ دیکھ سکیں ویجیلاائر کی رپورٹ کیسی ہوتی ہے۔ یہ صفحہ صرف نمائشی ہے۔ اصل اسکین کے لیے ملکیت کا ثبوت اور دستخط شدہ اجازت نامہ ضروری ہے۔",
        "scan_input": "ویب سائٹ کا پتہ",
        "scan_btn": "نمائشی چیک چلائیں",
        "scan_bad": "براہِ کرم درست ویب سائٹ پتہ درج کریں، مثلاً https://shop.example.pk",
        "scan_progress": ["پتے کی جانچ ہو رہی ہے...", "پبلک صفحات اور لاگ اِن فارمز کا نقشہ بن رہا ہے...", "معلوم کمزوریوں سے ملان ہو رہا ہے...", "شدت کے مطابق ترتیب دی جا رہی ہے..."],
        "scan_done": "نمائشی چیک مکمل ہوا برائے",
        "scan_demo_note": "یہ صرف نمائشی ڈیٹا ہے۔ آپ کی ویب سائٹ پر کوئی درخواست نہیں بھیجی گئی۔ اصل اسکین کے لیے سائن اپ کریں۔",
        "sev": {"Critical": "انتہائی خطرناک", "High": "زیادہ", "Medium": "درمیانہ"},
        "fix_label": "حل کا طریقہ",
        "why_label": "یہ کیوں اہم ہے",
        "threat_title": "خطرات کی انٹیلی جنس فیڈ",
        "threat_sub": "ویجیلاائر روزانہ CISA KEV، NVD اور CVE.org سے نئی اندراجات لیتا ہے، ہر صارف کے سافٹ ویئر سے ملاتا ہے اور اسکور دیتا ہے۔",
        "threat_src": [
            ("CISA KEV", "وہ کمزوریاں جو حقیقی حملوں میں استعمال ہو چکی ہیں", "سب سے اہم الرٹس"),
            ("NVD", "تفصیل، متاثرہ مصنوعات اور CVSS شدت اسکور", "ملان اور اسکورنگ"),
            ("CVE.org", "سرکاری شناخت نمبر اور مختصر تفصیل", "حوالہ اور دوہری جانچ"),
        ],
        "threat_head": ["CVE", "شدت", "خلاصہ", "ویجیلاائر کا اقدام"],
        "threat_rows": [
            ("CVE-2023-34362", "Critical", "فائل ٹرانسفر سافٹ ویئر میں SQL انجیکشن جو 2023 میں بڑے پیمانے پر استعمال ہوئی (MOVEit)۔", "مالک کو الرٹ؛ ورچوئل پیچ رول دستیاب"),
            ("CVE-2026-4891", "Critical", "پرانے ڈیٹا بیس ڈرائیور میں ریموٹ کوڈ ایگزیکیوشن۔", "حل کی رہنمائی کے ساتھ الرٹ"),
            ("CVE-2026-3102", "High", "ان پٹ کی کمزور جانچ کے باعث کراس سائٹ اسکرپٹنگ۔", "الرٹ بھیجا گیا؛ ان پٹ رول تجویز"),
            ("CVE-2026-1044", "Medium", "سیکیورٹی ہیڈر کی غلط کنفیگریشن۔", "ایک سطری حل کے ساتھ الرٹ"),
        ],
        "threat_note": "یہ نمائش کے لیے مثالی اندراجات ہیں۔ اصل فیڈ بزنس پلان میں بیان کردہ روزانہ پائپ لائن پر چلتی ہے۔",
        "block_title": "بلاکنگ انجن",
        "block_sub": "بلاکنگ ہمیشہ اختیاری، وقت کی حد کے ساتھ، لاگ شدہ اور ایک کلک میں واپس ہو سکتی ہے۔ ویجیلاائر پیشگی تحریری اجازت کے بغیر کسی اثاثے کو نہ جانچتا ہے نہ بلاک کرتا ہے۔",
        "modes_title": "اپنا بلاکنگ موڈ منتخب کریں",
        "modes": [
            ("صرف الرٹ", "تلاش کرتا اور خبردار کرتا ہے، کبھی بلاک نہیں کرتا۔ ہر نیا صارف یہاں سے شروع کر سکتا ہے۔"),
            ("اسٹینڈرڈ", "واضح حملے اور بار بار ناکام لاگ اِن بلاک کرتا ہے۔ تجویز کردہ ڈیفالٹ۔"),
            ("سخت", "درمیانے درجے کے شبہ والے نمونے بھی بلاک کرتا ہے۔ حملوں سے زیادہ محفوظ مگر اصل صارفین متاثر ہو سکتے ہیں۔"),
        ],
        "login_title": "لاگ اِن تحفظ (ابتدائی ڈیفالٹس)",
        "login_head": ["شرط", "اقدام"],
        "login_rows": [
            ("ایک اکاؤنٹ پر تین ناکام لاگ اِن", "اکاؤنٹ 15 منٹ کے لیے لاک اور مالک کو ای میل"),
            ("ایک IP تین اکاؤنٹس پر ناکام، یا دس منٹ میں دس بار", "IP ایک گھنٹے کے لیے بلاک (پاس ورڈ اسپرے کی روک تھام)"),
            ("بلاک کے بعد بھی کوششیں جاری", "24 گھنٹے، پھر 7 دن، پھر دستی جائزہ"),
            ("آپ کے اپنے دفتر کے IP ایڈریس", "اجازت فہرست میں، مگر نگرانی جاری"),
        ],
        "log_title": "انٹرسیپشن لاگ کی مثال",
        "log_note": "یہ صرف مثالی لاگ ہے۔ ہر اصل بلاک میں وقت، رول آئی ڈی، سورس IP اور اقدام درج ہوتا ہے۔",
        "limits_title": "ایماندارانہ حدود",
        "limits": [
            "کوئی سروس ہر حملہ نہیں روک سکتی، مثلاً درست چوری شدہ پاس ورڈ کا استعمال۔",
            "حملہ آور IP ایڈریس بدل سکتے ہیں، اس لیے پیٹرن پر مبنی شناخت ضروری ہے۔",
            "بہت بڑے ٹریفک حملوں (DDoS) کے لیے ماہر نیٹ ورک سطح کا تحفظ درکار ہے۔",
            "اگر ہمارا فلٹر بند ہو جائے تو آپ کی سائٹ چلتی رہتی ہے۔",
        ],
        "plans_title": "روپوں میں سادہ قیمتیں",
        "plans_sub": "ہر پلان میں بلاکنگ اور 14 دن کی مفت آزمائش شامل ہے۔ سالانہ ادائیگی پر 20% بچت۔",
        "per_month": "/ ماہ",
        "popular": "سب سے مقبول",
        "plans": [
            {"name": "اسٹارٹر", "price": "PKR 5,999", "usd": "تقریباً USD 21", "for": "ایک ویب سائٹ والے چھوٹے کاروبار", "feats": ["1 ویب سائٹ", "ہفتہ وار سیکیورٹی چیک", "حل کی رہنمائی کے ساتھ ای میل الرٹس", "لاگ اِن تحفظ (معاون پلیٹ فارمز)"], "btn": "مفت آزمائش شروع کریں"},
            {"name": "گروتھ", "price": "PKR 17,999", "usd": "تقریباً USD 64", "for": "وہ کاروبار جن کا کسٹمر ڈیٹا آن لائن ہے", "feats": ["5 تک سائٹس یا ڈیٹا بیس", "روزانہ سیکیورٹی چیک", "مشکوک کوئری کی مکمل بلاکنگ", "ماہانہ آسان زبان رپورٹ"], "btn": "مفت آزمائش شروع کریں", "popular": True},
            {"name": "بزنس", "price": "PKR 49,999", "usd": "تقریباً USD 179", "for": "وہ ادارے جنہیں کلائنٹس اور بینکوں کو ثبوت دینا ہے", "feats": ["20 تک اثاثے", "مسلسل چیک", "واٹس ایپ الرٹس اور سیفٹی سمری", "ورچوئل پیچنگ اور کسٹم رولز", "ترجیحی سپورٹ"], "btn": "سیلز سے بات کریں"},
            {"name": "ایجنسی", "price": "حسبِ ضرورت", "usd": "ری سیلر شرائط", "for": "ویب ایجنسیاں اور سافٹ ویئر ہاؤسز", "feats": ["ایک ساتھ کئی کلائنٹ سائٹس کا تحفظ", "ریفر کیے گئے صارفین پر کمیشن", "پارٹنر ڈیش بورڈ اور ماہانہ اسٹیٹمنٹ", "کو برانڈڈ رپورٹس"], "btn": "پارٹنر بنیں"},
        ],
        "extras_title": "مزید دستیاب",
        "extras": [
            ("سیکیورٹی آڈٹ", "PKR 60,000", "ایک ویب سائٹ: مکمل اسکین، اہم مسائل کی دستی جانچ، تحریری رپورٹ اور ایک دوبارہ جانچ۔"),
            ("سال میں دو بار آڈٹ پلان", "PKR 108,000", "12 مہینوں میں دو اسٹینڈرڈ آڈٹ۔"),
            ("توسیع شدہ آڈٹ", "PKR 200,000", "5 تک ویب سائٹس یا ڈیٹا بیس۔"),
        ],
        "toast": "شکریہ۔ یہ ڈیمو سائٹ ابھی سائن اپ نہیں لیتی، لیکن آپ کی دلچسپی نوٹ کر لی گئی ہے۔",
        "cta_title": "منٹوں میں اپنا خطرہ دیکھیں",
        "cta_sub": "مفت چیک چلائیں اور جانیں کہ حملہ آور کیا دیکھ سکتے ہیں۔",
        "footer": "ویجیلاائر کامسیٹس یونیورسٹی اسلام آباد، ایبٹ آباد کیمپس کا انٹرپرینیورشپ پروجیکٹ ہے۔ قیمتیں اور اعداد و شمار بزنس پلان 2026 کے منصوبہ بند تخمینے ہیں۔",
    },
}

# Demo findings for the free-check page (bilingual)
FINDINGS = [
    {"sev": "Critical", "en": ("SQL injection risk in a search or login form", "A visitor could read or change customer orders.", "Update the plug-in, use parameterised queries, then click Mark fixed to re-test."),
     "ur": ("سرچ یا لاگ اِن فارم میں SQL انجیکشن کا خطرہ", "کوئی بھی وزیٹر کسٹمر آرڈرز پڑھ یا بدل سکتا ہے۔", "پلگ اِن اپ ڈیٹ کریں، پیرامیٹرائزڈ کوئریز استعمال کریں، پھر دوبارہ جانچ کے لیے Mark fixed دبائیں۔")},
    {"sev": "Critical", "en": ("Database port open to the internet", "Anyone on the internet can try to connect to your data.", "Restrict database access to trusted addresses only in your hosting firewall."),
     "ur": ("ڈیٹا بیس پورٹ انٹرنیٹ پر کھلا ہے", "انٹرنیٹ پر کوئی بھی آپ کے ڈیٹا سے جڑنے کی کوشش کر سکتا ہے۔", "ہوسٹنگ فائر وال میں ڈیٹا بیس رسائی صرف قابلِ اعتماد ایڈریسز تک محدود کریں۔")},
    {"sev": "High", "en": ("Outdated CMS plug-in with a known weakness", "Attackers scan for this version automatically.", "Update the plug-in to the latest release and remove plug-ins you do not use."),
     "ur": ("پرانا CMS پلگ اِن جس میں معلوم کمزوری ہے", "حملہ آور اس ورژن کو خودکار طور پر تلاش کرتے ہیں۔", "پلگ اِن کو تازہ ترین ورژن پر اپ ڈیٹ کریں اور غیر استعمال شدہ پلگ اِنز ہٹا دیں۔")},
    {"sev": "High", "en": ("No limit on failed logins", "Attackers can guess passwords without being stopped.", "Turn on Vigilaire login protection and enable multi-factor authentication."),
     "ur": ("ناکام لاگ اِن پر کوئی حد نہیں", "حملہ آور بغیر رکاوٹ پاس ورڈ اندازے لگا سکتے ہیں۔", "ویجیلاائر لاگ اِن تحفظ آن کریں اور ملٹی فیکٹر تصدیق فعال کریں۔")},
    {"sev": "Medium", "en": ("Missing security headers", "Browsers get less help protecting your visitors.", "Add the recommended security headers in your web server settings."),
     "ur": ("سیکیورٹی ہیڈرز موجود نہیں", "براؤزرز کو آپ کے وزیٹرز کو بچانے میں کم مدد ملتی ہے۔", "اپنے ویب سرور کی سیٹنگز میں تجویز کردہ سیکیورٹی ہیڈرز شامل کریں۔")},
    {"sev": "Medium", "en": ("Certificate expires soon", "Visitors will see a warning and may leave.", "Renew the SSL certificate and turn on automatic renewal."),
     "ur": ("سرٹیفکیٹ جلد ختم ہونے والا ہے", "وزیٹرز کو وارننگ نظر آئے گی اور وہ چھوڑ سکتے ہیں۔", "SSL سرٹیفکیٹ کی تجدید کریں اور خودکار تجدید آن کریں۔")},
]

# ----------------------------------------------------------------------------
# Language selection (top of page)
# ----------------------------------------------------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

lang = st.session_state["lang"]
t = T[lang]
is_rtl = t["dir"] == "rtl"

# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Noto+Nastaliq+Urdu:wght@400;600;700&display=swap');

:root {
  --navy: #0A2540;
  --navy-2: #123B63;
  --blue: #1D6FB8;
  --teal: #0FA3A3;
  --teal-dark: #0B7C7C;
  --ink: #12263F;
  --muted: #4A6078;
  --line: #D9E3EE;
  --soft: #F3F7FB;
  --white: #FFFFFF;
  --crit: #B42318;
  --high: #B54708;
  --med: #8A6D00;
}

html { font-size: 18px; }
html, body, [class*="css"], .stApp {
  font-family: 'Manrope', 'Segoe UI', sans-serif !important;
  color: var(--ink);
}
.stApp { background: #FFFFFF; }

/* Hide default Streamlit chrome and sidebar */
header[data-testid="stHeader"], footer, #MainMenu,
[data-testid="stSidebar"], [data-testid="collapsedControl"],
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

.block-container {
  max-width: 1240px;
  padding: 1.2rem 2rem 3rem 2rem !important;
}

p, li { font-size: 1.08rem; line-height: 1.65; }
h1, h2, h3, h4 { color: var(--navy); letter-spacing: -0.01em; }

/* Top bar */
.topbar { display:flex; align-items:center; gap:14px; padding: 6px 0 10px 0; }
.logo {
  width: 54px; height: 54px; border-radius: 14px;
  background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
  display:flex; align-items:center; justify-content:center; font-size: 1.9rem;
  box-shadow: 0 6px 16px rgba(10,37,64,.25);
}
.brand { font-size: 2.1rem; font-weight: 800; color: var(--navy); line-height: 1; }
.brand-sub { font-size: 1rem; color: var(--muted); font-weight: 500; margin-top: 4px; }

/* Navigation pills (st.radio horizontal) */
div[role="radiogroup"] { gap: 8px; flex-wrap: wrap; }
div[role="radiogroup"] > label {
  background: var(--soft); border: 1px solid var(--line); border-radius: 999px;
  padding: 10px 22px; cursor: pointer; transition: all .15s ease;
}
div[role="radiogroup"] > label:hover { border-color: var(--blue); }
div[role="radiogroup"] > label > div:first-child { display: none !important; }
div[role="radiogroup"] > label p { font-size: 1.05rem !important; font-weight: 700; color: var(--navy); margin: 0; }
div[role="radiogroup"] > label:has(input:checked) { background: var(--navy); border-color: var(--navy); }
div[role="radiogroup"] > label:has(input:checked) p { color: #FFFFFF !important; }

/* Hero */
.hero {
  background: linear-gradient(120deg, #071B30 0%, #0A2540 45%, #0F4C81 100%);
  border-radius: 24px; padding: 64px 56px; margin: 18px 0 28px 0; color: #fff;
  position: relative; overflow: hidden;
}
.hero:after {
  content: ""; position:absolute; right:-120px; top:-120px; width: 420px; height: 420px;
  border-radius: 50%; background: radial-gradient(circle, rgba(15,163,163,.45), rgba(15,163,163,0) 65%);
}
.hero-tag {
  display:inline-block; font-size: 1rem; font-weight: 700; color: #BFEFEF;
  background: rgba(15,163,163,.22); border: 1px solid rgba(15,163,163,.55);
  padding: 7px 16px; border-radius: 999px; margin-bottom: 22px;
}
.hero h1 { color:#fff !important; font-size: 3.5rem; font-weight: 800; line-height: 1.12; margin: 0 0 20px 0; max-width: 860px; position: relative; z-index: 1; }
.hero p { color: #D6E4F2; font-size: 1.3rem; max-width: 780px; margin: 0; position: relative; z-index: 1; }

/* Stats */
.stats { display:grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 40px; }
.stat { border: 1px solid var(--line); border-radius: 18px; padding: 22px 24px; background: #fff; }
.stat b { display:block; font-size: 1.9rem; font-weight: 800; color: var(--navy); }
.stat span { font-size: 1rem; color: var(--muted); }

/* Section headings */
.sec-title { font-size: 2.4rem; font-weight: 800; color: var(--navy); margin: 34px 0 8px 0; }
.sec-sub { font-size: 1.2rem; color: var(--muted); margin-bottom: 26px; max-width: 900px; }

/* Cards */
.grid3 { display:grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.card { border: 1px solid var(--line); border-radius: 20px; padding: 30px; background: #fff; height: 100%; box-sizing: border-box; }
.card .ic { font-size: 2.2rem; margin-bottom: 12px; }
.card h3 { font-size: 1.5rem; margin: 0 0 10px 0; }
.card p { font-size: 1.08rem; color: var(--muted); margin: 0; }

/* Steps */
.steps { display:grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.step { background: var(--soft); border-radius: 18px; padding: 24px; display:flex; gap: 16px; align-items:flex-start; }
.step .n {
  min-width: 42px; height: 42px; border-radius: 50%; background: var(--navy); color:#fff;
  display:flex; align-items:center; justify-content:center; font-weight: 800; font-size: 1.15rem;
}
.step b { display:block; font-size: 1.2rem; color: var(--navy); margin-bottom: 4px; }
.step span { font-size: 1.02rem; color: var(--muted); }

/* Chips */
.chips { display:flex; flex-wrap:wrap; gap: 12px; }
.chip { background: #E7F6F6; color: var(--teal-dark); font-weight: 700; font-size: 1.05rem; padding: 10px 20px; border-radius: 999px; border: 1px solid #BFE6E6; }

/* Tables */
table.tbl { width:100%; border-collapse: separate; border-spacing: 0; border: 1px solid var(--line); border-radius: 16px; overflow:hidden; font-size: 1.05rem; }
table.tbl th { background: var(--navy); color:#fff; text-align: start; padding: 16px 18px; font-size: 1.05rem; }
table.tbl td { padding: 16px 18px; border-top: 1px solid var(--line); vertical-align: top; color: var(--ink); }
table.tbl tr:nth-child(even) td { background: var(--soft); }
table.tbl td.hl, table.tbl th.hl { background: #E7F6F6 !important; color: var(--navy); font-weight: 700; }
table.tbl th.hl { background: var(--teal-dark) !important; color: #fff; }

/* Severity badges */
.badge { display:inline-block; padding: 5px 14px; border-radius: 999px; font-weight: 800; font-size: .95rem; }
.b-Critical { background:#FDE7E4; color: var(--crit); }
.b-High { background:#FDEBD8; color: var(--high); }
.b-Medium { background:#FFF4CC; color: var(--med); }

/* Findings */
.finding { border: 1px solid var(--line); border-inline-start: 6px solid var(--blue); border-radius: 14px; padding: 22px 24px; margin-bottom: 14px; background:#fff; }
.finding.Critical { border-inline-start-color: var(--crit); }
.finding.High { border-inline-start-color: #E0781E; }
.finding.Medium { border-inline-start-color: #D4A900; }
.finding h4 { font-size: 1.3rem; margin: 10px 0 8px 0; }
.finding p { margin: 4px 0; font-size: 1.05rem; color: var(--ink); }

/* Pricing */
.plan { border: 1.5px solid var(--line); border-radius: 22px; padding: 32px 26px; background:#fff; height: 100%; box-sizing: border-box; position: relative; }
.plan.pop { border-color: var(--teal); box-shadow: 0 14px 34px rgba(15,163,163,.18); }
.pop-badge { position:absolute; top:-15px; inset-inline-start: 24px; background: var(--teal); color:#fff; font-weight: 800; padding: 6px 16px; border-radius: 999px; font-size: .95rem; }
.plan h3 { font-size: 1.6rem; margin: 0 0 4px 0; }
.plan .for { color: var(--muted); font-size: 1rem; min-height: 54px; }
.plan .price { font-size: 2.4rem; font-weight: 800; color: var(--navy); margin-top: 8px; }
.plan .per { font-size: 1.05rem; color: var(--muted); font-weight: 600; }
.plan .usd { color: var(--muted); font-size: .98rem; margin-bottom: 14px; }
.plan ul { padding-inline-start: 20px; margin: 14px 0 0 0; }
.plan li { font-size: 1.05rem; margin-bottom: 8px; }

/* Buttons */
.stButton > button {
  width: 100%; background: var(--navy); color: #fff; border: none; border-radius: 12px;
  padding: 14px 18px; font-size: 1.1rem; font-weight: 700; font-family: inherit;
}
.stButton > button:hover { background: var(--blue); color:#fff; border: none; }
.stButton > button:focus-visible { outline: 3px solid var(--teal); }
.stButton > button p { font-size: 1.1rem !important; font-weight: 700; color: #fff; }

/* Inputs */
.stTextInput input { font-size: 1.15rem !important; padding: 14px 16px !important; border-radius: 12px !important; }
.stTextInput label p { font-size: 1.1rem !important; font-weight: 700; color: var(--navy); }

/* Call to action band */
.cta { background: linear-gradient(120deg, var(--navy) 0%, var(--navy-2) 100%); border-radius: 22px; padding: 44px 48px; color:#fff; margin-top: 40px; }
.cta h2 { color:#fff !important; font-size: 2.2rem; margin: 0 0 8px 0; }
.cta p { color:#D6E4F2; font-size: 1.2rem; margin: 0; }

/* Misc */
.note { background: var(--soft); border: 1px solid var(--line); border-radius: 12px; padding: 14px 18px; color: var(--muted); font-size: 1rem; margin-top: 14px; }
.logbox { background:#0A1B2D; color:#CFE3F5; border-radius: 16px; padding: 22px 26px; font-family: 'Courier New', monospace; font-size: 1rem; line-height: 1.9; direction: ltr; text-align: left; overflow-x:auto; }
.logbox .bl { color:#FF8A80; font-weight:700; }
.logbox .mt { color:#FFD580; font-weight:700; }
.footer { margin-top: 56px; padding-top: 24px; border-top: 1px solid var(--line); color: var(--muted); font-size: .98rem; }

/* Responsive */
@media (max-width: 900px) {
  .block-container { padding: 1rem 1rem 2rem 1rem !important; }
  .hero { padding: 38px 24px; }
  .hero h1 { font-size: 2.3rem; }
  .hero p { font-size: 1.12rem; }
  .stats { grid-template-columns: repeat(2, 1fr); }
  .grid3, .steps { grid-template-columns: 1fr; }
  .sec-title { font-size: 1.9rem; }
  .cta { padding: 30px 24px; }
}
</style>
"""

RTL_CSS = """
<style>
html, body, [class*="css"], .stApp, p, li, td, th, h1, h2, h3, h4, label, input, button {
  font-family: 'Noto Nastaliq Urdu', 'Manrope', serif !important;
}
.block-container { direction: rtl; text-align: right; }
p, li { line-height: 2.1 !important; }
.hero h1 { line-height: 1.7 !important; }
.sec-title { line-height: 1.7; }
.card h3, .plan h3, .finding h4 { line-height: 1.8; }
.stTextInput input { direction: ltr; text-align: left; }
.logbox { font-family: 'Courier New', monospace !important; }
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)
if is_rtl:
    st.markdown(RTL_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header: brand, language, navigation
# ----------------------------------------------------------------------------
left, right = st.columns([3, 1.4])
with left:
    st.markdown(
        h(f"""
        <div class="topbar">
          <div class="logo">🛡️</div>
          <div>
            <div class="brand">{"ویجیلاائر" if is_rtl else "Vigilaire"}</div>
            <div class="brand-sub">{t["tagline"]}</div>
          </div>
        </div>
        """),
        unsafe_allow_html=True,
    )
with right:
    st.radio(
        "Language",
        ["English", "اردو"],
        key="lang",
        horizontal=True,
        label_visibility="collapsed",
    )

NAV_KEYS = ["overview", "scan", "threat", "block", "plans"]
page = st.radio(
    "Navigation",
    NAV_KEYS,
    format_func=lambda k: t["nav"][k],
    horizontal=True,
    label_visibility="collapsed",
    key="page",
)


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def table(head, rows, highlight_col=None, badge_col=None):
    out = ['<table class="tbl"><thead><tr>']
    for i, c in enumerate(head):
        cls = ' class="hl"' if i == highlight_col else ""
        out.append(f"<th{cls}>{c}</th>")
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>")
        for i, c in enumerate(r):
            if i == badge_col:
                label = t["sev"].get(c, c)
                out.append(f'<td><span class="badge b-{c}">{label}</span></td>')
            else:
                cls = ' class="hl"' if i == highlight_col else ""
                out.append(f"<td{cls}>{c}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def title(text, sub=None):
    st.markdown(f'<div class="sec-title">{text}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="sec-sub">{sub}</div>', unsafe_allow_html=True)


def cta_band():
    st.markdown(
        h(f"""
        <div class="cta">
          <h2>{t["cta_title"]}</h2>
          <p>{t["cta_sub"]}</p>
        </div>
        """),
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(f'<div class="footer">{t["footer"]}</div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
if page == "overview":
    st.markdown(
        h(f"""
        <div class="hero">
          <div class="hero-tag">🛡️ {t["tagline"]}</div>
          <h1>{t["hero_title"]}</h1>
          <p>{t["hero_sub"]}</p>
        </div>
        """),
        unsafe_allow_html=True,
    )

    stats_html = "".join(f"<div class='stat'><b>{a}</b><span>{b}</span></div>" for a, b in t["stats"])
    st.markdown(f'<div class="stats">{stats_html}</div>', unsafe_allow_html=True)

    title(t["three_title"], t["three_sub"])
    cards_html = "".join(
        f"<div class='card'><div class='ic'>{ic}</div><h3>{ti}</h3><p>{de}</p></div>"
        for ic, ti, de in t["cards"]
    )
    st.markdown(f'<div class="grid3">{cards_html}</div>', unsafe_allow_html=True)

    title(t["how_title"], t["how_sub"])
    steps_html = "".join(
        f"<div class='step'><div class='n'>{i}</div><div><b>{a}</b><span>{b}</span></div></div>"
        for i, (a, b) in enumerate(t["steps"], 1)
    )
    st.markdown(f'<div class="steps">{steps_html}</div>', unsafe_allow_html=True)

    title(t["who_title"])
    chips = "".join(f"<span class='chip'>{c}</span>" for c in t["who"])
    st.markdown(f'<div class="chips">{chips}</div>', unsafe_allow_html=True)

    title(t["cmp_title"])
    st.markdown(table(t["cmp_head"], t["cmp_rows"], highlight_col=3), unsafe_allow_html=True)

    title(t["kpi_title"])
    c1, c2, c3, c4 = st.columns(4)
    for col, (label, value, delta) in zip((c1, c2, c3, c4), t["kpis"]):
        col.metric(label, value, delta, delta_color="off")
    st.markdown(f'<div class="note">{t["kpi_note"]}</div>', unsafe_allow_html=True)

    cta_band()
    footer()

elif page == "scan":
    title(t["scan_title"], t["scan_sub"])

    url = st.text_input(t["scan_input"], placeholder="https://shop.example.pk")
    run = st.button(t["scan_btn"], key="run_scan")

    if run:
        pattern = r"^(https?://)?([A-Za-z0-9-]+\.)+[A-Za-z]{2,}(/.*)?$"
        if not url or not re.match(pattern, url.strip()):
            st.error(t["scan_bad"])
        else:
            target = url.strip()
            bar = st.progress(0)
            status = st.empty()
            for i, msg in enumerate(t["scan_progress"]):
                status.markdown(f"**{msg}**")
                bar.progress(int((i + 1) / len(t["scan_progress"]) * 100))
                time.sleep(0.6)
            status.empty()
            bar.empty()

            # Deterministic demo results derived from the address
            digest = int(hashlib.sha256(target.lower().encode()).hexdigest(), 16)
            count = 3 + digest % 3
            start = digest % len(FINDINGS)
            picked = [FINDINGS[(start + i) % len(FINDINGS)] for i in range(count)]
            picked.sort(key=lambda f: ["Critical", "High", "Medium"].index(f["sev"]))

            st.success(f"{t['scan_done']} {target}")
            counts = {s: sum(1 for f in picked if f["sev"] == s) for s in ("Critical", "High", "Medium")}
            m1, m2, m3 = st.columns(3)
            m1.metric(t["sev"]["Critical"], counts["Critical"])
            m2.metric(t["sev"]["High"], counts["High"])
            m3.metric(t["sev"]["Medium"], counts["Medium"])

            key = "ur" if is_rtl else "en"
            for f in picked:
                ti, why, fix = f[key]
                st.markdown(
                    h(f"""
                    <div class="finding {f['sev']}">
                      <span class="badge b-{f['sev']}">{t['sev'][f['sev']]}</span>
                      <h4>{ti}</h4>
                      <p><b>{t['why_label']}:</b> {why}</p>
                      <p><b>{t['fix_label']}:</b> {fix}</p>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )
            st.markdown(f'<div class="note">{t["scan_demo_note"]}</div>', unsafe_allow_html=True)

    footer()

elif page == "threat":
    title(t["threat_title"], t["threat_sub"])
    src_html = "".join(
        f"<div class='card'><h3>{a}</h3><p>{b}</p><p style='margin-top:10px'><b>{c}</b></p></div>"
        for a, b, c in t["threat_src"]
    )
    st.markdown(f'<div class="grid3">{src_html}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown(table(t["threat_head"], t["threat_rows"], badge_col=1), unsafe_allow_html=True)
    st.markdown(f'<div class="note">{t["threat_note"]}</div>', unsafe_allow_html=True)
    footer()

elif page == "block":
    title(t["block_title"], t["block_sub"])

    st.markdown(f'<h3 style="font-size:1.7rem">{t["modes_title"]}</h3>', unsafe_allow_html=True)
    icons = ["👁️", "🛡️", "🔒"]
    modes_html = "".join(
        f"<div class='card'><div class='ic'>{icons[i]}</div><h3>{a}</h3><p>{b}</p></div>"
        for i, (a, b) in enumerate(t["modes"])
    )
    st.markdown(f'<div class="grid3">{modes_html}</div>', unsafe_allow_html=True)

    st.markdown(f'<h3 style="font-size:1.7rem;margin-top:36px">{t["login_title"]}</h3>', unsafe_allow_html=True)
    st.markdown(table(t["login_head"], t["login_rows"]), unsafe_allow_html=True)

    st.markdown(f'<h3 style="font-size:1.7rem;margin-top:36px">{t["log_title"]}</h3>', unsafe_allow_html=True)
    st.markdown(
        h("""
        <div class="logbox">
        <span class="bl">[BLOCKED]</span> 203.0.113.12 &nbsp;SQL injection pattern on /login &nbsp;(rule R-014, 1 h)<br>
        <span class="bl">[BLOCKED]</span> 198.51.100.44 &nbsp;Repeated failed logins on 3 accounts &nbsp;(rule L-002, 1 h)<br>
        <span class="mt">[WATCHING]</span> 192.0.2.77 &nbsp;Unusual request pattern, owner notified, no block<br>
        <span class="mt">[SLOWED]</span> 198.51.100.9 &nbsp;Very fast probing, rate limit applied
        </div>
        """),
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="note">{t["log_note"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<h3 style="font-size:1.7rem;margin-top:36px">{t["limits_title"]}</h3>', unsafe_allow_html=True)
    for item in t["limits"]:
        st.markdown(f"- {item}")
    footer()

elif page == "plans":
    title(t["plans_title"], t["plans_sub"])

    cols = st.columns(4, gap="medium")
    for i, (col, p) in enumerate(zip(cols, t["plans"])):
        with col:
            pop = p.get("popular", False)
            badge = f'<div class="pop-badge">{t["popular"]}</div>' if pop else ""
            per = "" if p["price"] in ("Custom", "حسبِ ضرورت") else f' <span class="per">{t["per_month"]}</span>'
            feats = "".join(f"<li>{f}</li>" for f in p["feats"])
            st.markdown(
                h(f"""
                <div class="plan {'pop' if pop else ''}">
                  {badge}
                  <h3>{p['name']}</h3>
                  <div class="for">{p['for']}</div>
                  <div class="price">{p['price']}{per}</div>
                  <div class="usd">{p['usd']}</div>
                  <ul>{feats}</ul>
                </div>
                """),
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            if st.button(p["btn"], key=f"plan_{i}"):
                st.toast(t["toast"], icon="✅")

    title(t["extras_title"])
    e_html = "".join(
        f"<div class='card'><h3>{a}</h3><div class='price' style='font-size:1.8rem;font-weight:800;color:#0A2540;margin-bottom:8px'>{b}</div><p>{c}</p></div>"
        for a, b, c in t["extras"]
    )
    st.markdown(f'<div class="grid3">{e_html}</div>', unsafe_allow_html=True)

    cta_band()
    footer()

