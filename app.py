import streamlit as st
import json
import os
from datetime import datetime, date, timedelta, timezone
import urllib.parse

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Yurt Menü",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- TIMEZONE & HELPERS (Turkey UTC+3) -----------------
TURKEY_TZ = timezone(timedelta(hours=3))

def get_turkey_now() -> datetime:
    return datetime.now(TURKEY_TZ)

def get_turkey_today() -> date:
    return get_turkey_now().date()

TURKISH_DAYS = {
    0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
    4: "Cuma", 5: "Cumartesi", 6: "Pazar"
}
TURKISH_DAYS_SHORT = {
    0: "Pzt", 1: "Sal", 2: "Çar", 3: "Per",
    4: "Cum", 5: "Cmt", 6: "Paz"
}
TURKISH_MONTHS = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}

def format_date_tr(d: date) -> str:
    day_name = TURKISH_DAYS.get(d.weekday(), "")
    month_name = TURKISH_MONTHS.get(d.month, "")
    return f"{d.day} {month_name}, {day_name}"

DATA_FILE = os.path.join(os.path.dirname(__file__), "menu_data.json")

def load_menu_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"dorm_name": "Yurt Yemekhanesi", "meals": {}}

menu_db = load_menu_data()
available_dates = sorted(menu_db.get("meals", {}).keys())

DEFAULT_DATE = date(2026, 11, 12)
if available_dates:
    try:
        first_d = datetime.strptime(available_dates[0], "%Y-%m-%d").date()
        last_d = datetime.strptime(available_dates[-1], "%Y-%m-%d").date()
    except Exception:
        first_d, last_d = date(2026, 11, 1), date(2026, 11, 30)
else:
    first_d, last_d = date(2026, 11, 1), date(2026, 11, 30)

# ----------------- MODERN AEROVOLT-INSPIRED CSS -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Force Light Theme Canvas regardless of browser / OS Dark Mode */
    :root, [data-theme="dark"], [data-theme="light"], html, body {
        color-scheme: light !important;
    }

    html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, [data-testid="stHeader"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0A0A0A !important;
        -webkit-font-smoothing: antialiased;
    }

    #MainMenu, header, footer { display: none !important; }
    .stDeployButton { display: none !important; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }

    /* Top Brand Bar */
    .aero-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0 1.1rem 0;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 1.1rem;
    }
    .aero-logo {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #0A0A0A;
    }
    .aero-badge-pill {
        background: #F0F9FF;
        color: #0369A1;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid #BAE6FD;
        letter-spacing: 0.02em;
    }

    /* Fixed Modern Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        background-color: #F8FAFC !important;
        padding: 4px !important;
        border-radius: 14px !important;
        border: 1px solid #E2E8F0 !important;
        justify-content: space-around !important;
        margin-bottom: 1.2rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        padding: 8px 16px !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.15s ease !important;
    }
    .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span {
        color: #64748B !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06) !important;
    }
    .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {
        color: #0284C7 !important;
        font-weight: 800 !important;
    }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Hero Headline (Mobile Optimized & Centered) */
    .hero-title-box {
        margin-top: 0.6rem;
        margin-bottom: 0.9rem;
        text-align: center;
    }
    .hero-kicker {
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748B;
        margin-bottom: 3px;
    }
    .hero-h1 {
        font-size: 1.3rem !important;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.2 !important;
        color: #0A0A0A;
        margin-bottom: 0.35rem;
        white-space: nowrap !important;
        text-align: center;
    }
    
    /* Ice-Blue Pill Banner (Responsive Flex Wrap) */
    .ice-pill-banner {
        display: inline-flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 6px;
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 999px;
        padding: 5px 12px;
        font-size: 0.74rem;
        font-weight: 700;
        color: #0284C7;
        line-height: 1.35;
        margin: 0 auto;
        text-align: center;
    }
    .ice-pill-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #0284C7;
        display: inline-block;
        flex-shrink: 0;
    }

    /* Symmetrical Mobile 3-Button Navigation Bar */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 8px !important;
        width: 100% !important;
        margin-bottom: 0.6rem !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 0px !important;
        min-width: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stButton"] {
        width: 100% !important;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 0 4px !important;
        min-height: 42px !important;
        height: 42px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FFFFFF !important;
        color: #0A0A0A !important;
        transition: all 0.15s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }
    div[data-testid="stButton"] button p {
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
        margin: 0 !important;
        text-align: center !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #F8FAFC !important;
        border-color: #0A0A0A !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #0A0A0A !important;
        color: #FFFFFF !important;
        border-color: #0A0A0A !important;
    }
    div[data-testid="stButton"] button[kind="primary"] p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Modern Card Sections */
    .meal-card-group {
        display: flex;
        flex-direction: column;
        gap: 1.2rem;
        margin-bottom: 1.4rem;
    }

    .aero-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 20px;
        padding: 1.25rem 1.15rem;
        box-shadow: 0 4px 20px -4px rgba(10, 10, 10, 0.03);
        margin-bottom: 1.1rem;
    }
    .aero-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.75rem;
        margin-bottom: 0.85rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .aero-card-title {
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0A0A0A;
    }
    .aero-card-badge {
        font-size: 0.7rem;
        font-weight: 700;
        color: #475569;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 3px 9px;
        border-radius: 999px;
    }

    /* Food Item Rows */
    .aero-food-item {
        display: flex;
        align-items: center;
        padding: 0.65rem 0.85rem;
        background: #F8FAFC;
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        margin-bottom: 0.45rem;
        box-sizing: border-box;
    }
    .aero-food-item:last-child {
        margin-bottom: 0;
    }
    .aero-food-index {
        font-size: 0.72rem;
        font-weight: 800;
        color: #94A3B8;
        width: 26px;
        flex-shrink: 0;
        letter-spacing: 0.02em;
    }
    .aero-food-name {
        font-size: 0.92rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.01em;
        flex-grow: 1;
    }
    .aero-food-arrow {
        font-size: 0.85rem;
        font-weight: 700;
        color: #CBD5E1;
        padding-left: 6px;
    }

    /* Snack Box (Weekend Special) */
    .aero-snack-card {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 14px;
        padding: 0.75rem 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 0.8rem;
    }
    .aero-snack-tag {
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        color: #15803D;
        background: #DCFCE7;
        padding: 2px 8px;
        border-radius: 6px;
        letter-spacing: 0.05em;
    }
    .aero-snack-text {
        font-size: 0.9rem;
        font-weight: 700;
        color: #14532D;
    }

    /* Stats Strip */
    .stats-strip {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        padding: 0.9rem 0;
        border-top: 1px solid #F1F5F9;
        border-bottom: 1px solid #F1F5F9;
        margin: 1.2rem 0;
    }
    .stat-item {
        text-align: center;
    }
    .stat-number {
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #0A0A0A;
    }
    .stat-desc {
        font-size: 0.66rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }

    /* WhatsApp Button */
    .aero-cta-black {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        background-color: #0A0A0A;
        color: #FFFFFF !important;
        text-decoration: none;
        padding: 0.75rem 1.2rem;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin-top: 0.9rem;
        box-sizing: border-box;
    }

    /* Radio Group Pill */
    div[data-testid="stRadio"] {
        background-color: transparent !important;
    }
    div[data-testid="stRadio"] > div {
        background: #F8FAFC !important;
        padding: 4px 12px !important;
        border-radius: 999px !important;
        border: 1px solid #E2E8F0 !important;
        gap: 12px !important;
        justify-content: center !important;
        margin-bottom: 1.2rem !important;
    }
    div[data-testid="stRadio"] label {
        color: #0A0A0A !important;
    }
    div[data-testid="stRadio"] label p {
        color: #0A0A0A !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
    }

    /* Popover Date Button */
    div[data-testid="stPopover"] {
        width: 100% !important;
        margin-bottom: 1rem !important;
    }
    div[data-testid="stPopover"] button {
        width: 100% !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        background: #F8FAFC !important;
        border: 1px dashed #CBD5E1 !important;
        color: #475569 !important;
        height: 38px !important;
        min-height: 38px !important;
    }

    /* Search Results */
    .search-card-aero {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }
    .search-header-row {
        font-size: 0.78rem;
        font-weight: 800;
        color: #0284C7;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE & DATE INITIALIZATION -----------------
today_tr = get_turkey_today()
if "selected_date" not in st.session_state or not isinstance(st.session_state.selected_date, date):
    if first_d <= today_tr <= last_d:
        st.session_state.selected_date = today_tr
    else:
        st.session_state.selected_date = DEFAULT_DATE

if st.session_state.selected_date < first_d:
    st.session_state.selected_date = first_d
elif st.session_state.selected_date > last_d:
    st.session_state.selected_date = last_d

sel_date = st.session_state.selected_date
current_date_str = sel_date.strftime("%Y-%m-%d")

# ----------------- BRAND NAVBAR (Accurate Turkey Time) -----------------
dorm_title = menu_db.get("dorm_name", "Yurt Yemekhanesi")
now = get_turkey_now()

st.markdown(f"""
<div class="aero-nav">
    <div class="aero-logo">{dorm_title}</div>
    <div class="aero-badge-pill">{now.strftime("%H:%M")} / Canlı</div>
</div>
""", unsafe_allow_html=True)

# ----------------- MAIN TABS -----------------
tab_today, tab_all = st.tabs(["Günün Menüsü", "Aylık Liste & Arama"])

# ----------------- TAB 1: GÜNÜN MENÜSÜ -----------------
with tab_today:
    # Symmetrical 3-Button Navigation: [‹ Dün] [⭐ Bugün] [Yarın ›]
    c_prev, c_today, c_next = st.columns([1, 1.2, 1])
    with c_prev:
        if st.button("‹ Dün", use_container_width=True):
            if sel_date > first_d:
                st.session_state.selected_date = sel_date - timedelta(days=1)
                st.rerun()
    with c_today:
        is_curr_today = (sel_date == today_tr)
        if st.button("⭐ Bugün", use_container_width=True, type="primary" if is_curr_today else "secondary"):
            st.session_state.selected_date = today_tr if (first_d <= today_tr <= last_d) else DEFAULT_DATE
            st.rerun()
    with c_next:
        if st.button("Yarın ›", use_container_width=True):
            if sel_date < last_d:
                st.session_state.selected_date = sel_date + timedelta(days=1)
                st.rerun()

    # Active Day Hero Header & Dynamic Meal Hours
    formatted_date_str = format_date_tr(sel_date)
    is_today_match = (sel_date == today_tr)
    day_badge_label = "GÜNÜN MENÜSÜ" if is_today_match else f"{TURKISH_DAYS.get(sel_date.weekday(), '').upper()} GÜNÜ"
    
    # Weekday vs Weekend Meal Hours
    is_weekend = (sel_date.weekday() >= 5)
    breakfast_hours = "09:00 — 11:30" if is_weekend else "07:00 — 09:00"
    dinner_hours = "18:00 — 20:00"
    day_type_label = "Hafta Sonu" if is_weekend else "Hafta İçi"

    st.markdown(f"""
    <div class="hero-title-box">
        <div class="hero-kicker">{day_badge_label} • {day_type_label.upper()}</div>
        <div class="hero-h1">{formatted_date_str}</div>
        <div class="ice-pill-banner">
            <span class="ice-pill-dot"></span>
            <span>Kahvaltı: {breakfast_hours} &nbsp;|&nbsp; Akşam: {dinner_hours}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean date jump popover
    with st.popover("📅 Başka bir günün menüsüne bak", use_container_width=True):
        picked_d = st.date_input(
            "Tarih Seç",
            value=sel_date,
            min_value=first_d,
            max_value=last_d,
            label_visibility="collapsed"
        )
        if picked_d != sel_date:
            st.session_state.selected_date = picked_d
            st.rerun()

    # Segmented Control: [Tümü, Kahvaltı, Akşam]
    filter_choice = st.radio(
        "Öğün Seçimi",
        ["Tümü", "Kahvaltı", "Akşam Yemeği"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Fetch meal data
    day_data = menu_db.get("meals", {}).get(current_date_str, {})
    breakfast_list = day_data.get("breakfast", [])
    dinner_list = day_data.get("dinner", [])
    snack_item = day_data.get("snack")

    show_b = filter_choice in ["Tümü", "Kahvaltı"] and len(breakfast_list) > 0
    show_d = filter_choice in ["Tümü", "Akşam Yemeği"] and len(dinner_list) > 0

    if not show_b and not show_d:
        st.info("Bu tarih için kayıtlı menü bulunamadı.")
    else:
        # --- KAHVALTI KARTI (Zero indentation to prevent markdown code block bug) ---
        if show_b:
            b_items_html = "".join([
                f'<div class="aero-food-item">'
                f'<span class="aero-food-index">{i:02d}</span>'
                f'<span class="aero-food-name">{itm}</span>'
                f'<span class="aero-food-arrow">›</span>'
                f'</div>'
                for i, itm in enumerate(breakfast_list, 1)
            ])

            snack_html = ""
            if snack_item:
                snack_html = (
                    f'<div class="aero-snack-card">'
                    f'<span class="aero-snack-tag">Ara Öğün</span>'
                    f'<span class="aero-snack-text">{snack_item}</span>'
                    f'</div>'
                )

            card_b_html = (
                f'<div class="aero-card">'
                f'<div class="aero-card-header">'
                f'<span class="aero-card-title">Kahvaltı</span>'
                f'<span class="aero-card-badge">{breakfast_hours}</span>'
                f'</div>'
                f'{b_items_html}'
                f'{snack_html}'
                f'</div>'
            )
            st.markdown(card_b_html, unsafe_allow_html=True)

        # --- AKŞAM YEMEĞİ KARTI (Zero indentation to prevent markdown code block bug) ---
        if show_d:
            d_items_html = "".join([
                f'<div class="aero-food-item">'
                f'<span class="aero-food-index">{i:02d}</span>'
                f'<span class="aero-food-name">{itm}</span>'
                f'<span class="aero-food-arrow">›</span>'
                f'</div>'
                for i, itm in enumerate(dinner_list, 1)
            ])

            card_d_html = (
                f'<div class="aero-card">'
                f'<div class="aero-card-header">'
                f'<span class="aero-card-title">Akşam Yemeği</span>'
                f'<span class="aero-card-badge">{dinner_hours}</span>'
                f'</div>'
                f'{d_items_html}'
                f'</div>'
            )
            st.markdown(card_d_html, unsafe_allow_html=True)

        # Stats Strip
        st.markdown("""
        <div class="stats-strip">
            <div class="stat-item">
                <div class="stat-number">2</div>
                <div class="stat-desc">Günlük Servis</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">Kasım</div>
                <div class="stat-desc">Dönem</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">30 Gün</div>
                <div class="stat-desc">Tam Liste</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # WhatsApp Share
        wa_text = f"*{dorm_title} Menüsü - {formatted_date_str}*\n\n"
        if breakfast_list:
            wa_text += "KAHVALTI:\n" + "\n".join([f"• {x}" for x in breakfast_list]) + "\n\n"
        if snack_item:
            wa_text += f"ARA ÖĞÜN: {snack_item}\n\n"
        if dinner_list:
            wa_text += "AKŞAM YEMEĞİ:\n" + "\n".join([f"• {x}" for x in dinner_list])

        wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_text)}"

        st.markdown(f"""
        <a href="{wa_url}" target="_blank" class="aero-cta-black">
            WhatsApp ile Paylaş
        </a>
        """, unsafe_allow_html=True)


# ----------------- TAB 2: AYLIK LİSTE & ARAMA -----------------
with tab_all:
    search_term = st.text_input(
        "Arama",
        placeholder="Yemek veya ürün ara (örn: kruvasan, alinazik, tavuk, pide)...",
        label_visibility="collapsed"
    )

    clean_term = search_term.strip().lower() if search_term else ""
    meals_dict = menu_db.get("meals", {})

    if clean_term:
        match_count = 0
        st.caption(f"'{clean_term}' için bulunan sonuçlar:")

        for d_key in sorted(meals_dict.keys()):
            d_info = meals_dict[d_key]
            b_items = d_info.get("breakfast", [])
            d_items = d_info.get("dinner", [])
            snk = d_info.get("snack") or ""

            b_match = any(clean_term in x.lower() for x in b_items)
            d_match = any(clean_term in x.lower() for x in d_items)
            s_match = clean_term in snk.lower()

            if b_match or d_match or s_match:
                match_count += 1
                try:
                    dt = datetime.strptime(d_key, "%Y-%m-%d").date()
                    day_str = format_date_tr(dt)
                except Exception:
                    day_str = d_key

                res_html = (
                    f'<div class="search-card-aero">'
                    f'<div class="search-header-row">{day_str}</div>'
                    f'<div style="font-size:0.88rem; color:#0A0A0A; line-height:1.45;">'
                    f'{"<strong>Kahvaltı:</strong> " + ", ".join(b_items) + "<br>" if b_match or not d_match else ""}'
                    f'{"<strong>Akşam:</strong> " + ", ".join(d_items) if d_match or not b_match else ""}'
                    f'</div></div>'
                )
                st.markdown(res_html, unsafe_allow_html=True)

        if match_count == 0:
            st.info("Aradığınız yemek menüde bulunamadı.")
    else:
        st.markdown("##### Kasım 2026 Tam Liste")
        for d_key in sorted(meals_dict.keys()):
            d_info = meals_dict[d_key]
            try:
                dt = datetime.strptime(d_key, "%Y-%m-%d").date()
                day_str = format_date_tr(dt)
            except Exception:
                day_str = d_key

            b_items = d_info.get("breakfast", [])
            d_items = d_info.get("dinner", [])
            snk = d_info.get("snack")

            preview_dish = d_items[1] if len(d_items) > 1 else (d_items[0] if d_items else "Menü")
            with st.expander(f"{day_str} — {preview_dish}"):
                if b_items:
                    st.markdown("**Kahvaltı:**")
                    for x in b_items:
                        st.markdown(f"- {x}")
                if snk:
                    st.markdown(f"**Ara Öğün:** {snk}")
                if d_items:
                    st.markdown("**Akşam Yemeği:**")
                    for x in d_items:
                        st.markdown(f"- {x}")
