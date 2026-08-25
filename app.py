import streamlit as st
from PIL import Image
import math

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CAD/CAM Machining Cost & Hardening Estimator",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS: HIGH-TECH ENGINEERING DASHBOARD ---
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    .eng-header {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid #0284c7;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    .eng-title {
        font-size: 28px;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: 0.5px;
        margin: 0;
    }
    .eng-subtitle {
        font-size: 14px;
        color: #38bdf8;
        margin-top: 4px;
        font-weight: 500;
    }

    .section-header {
        font-size: 16px;
        font-weight: 700;
        color: #38bdf8;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 15px;
        margin-bottom: 15px;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #0284c7;
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 22px;
        font-weight: 800;
        color: #f1f5f9;
        margin-top: 5px;
    }
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .quote-banner {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        padding: 24px;
        border-radius: 14px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 12px 20px -4px rgba(2, 132, 199, 0.4);
        border: 1px solid #38bdf8;
    }
    .quote-price {
        font-size: 38px;
        font-weight: 900;
        letter-spacing: 1px;
        margin-top: 6px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# --- KAMUS BAHASA ---
LANG = {
    "ID": {
        "title": "⚙️ MACHINING & HEAT TREATMENT COST ESTIMATOR",
        "subtitle": "SYSTEM COST CALCULATOR & CYCLE TIME ANALYZER — POWERED FOR BANG BOY",
        "setting_rates": "🛠️ PARAMETER & TARIF MESIN",
        "rate_bubut_man": "Tarif Bubut Manual (Rp/Jam)",
        "rate_bubut_cnc": "Tarif Bubut CNC (Rp/Jam)",
        "rate_mill_man": "Tarif Milling Manual (Rp/Jam)",
        "rate_mill_cnc": "Tarif Milling CNC / VMC (Rp/Jam)",
        "rate_surf_grind": "Tarif Surface Grinding (Rp/Jam)",
        "rate_cyl_grind": "Tarif Cylindrical Grinding (Rp/Jam)",
        "rate_hardening": "Tarif Hardening (Rp/kg)",
        "min_hardening": "Min. Charge Hardening (Rp)",
        "margin": "Target Profit Margin (%)",
        "doc_title": "📷 WORKPIECE DRAWING / PHOTO",
        "img_source": "Sumber Gambar Part:",
        "cam_opt": "Kamera Direct",
        "upload_opt": "Upload FILE CAD/Foto",
        "cam_label": "Ambil Foto Benda Kerja",
        "calc_title": "🧮 AUTOMATIC CYCLE TIME CALCULATOR",
        "tab_lathe": "🌀 Turning (Bubut)",
        "tab_mill": "🔲 Milling",
        "tab_s_grind": "⬛ Surface Grinding",
        "tab_c_grind": "⭕ Cylindrical Grinding",
        "form_title": "📋 DETAIL SPESIFIKASI & KOSTING",
        "sec_mat": "1. MATERIAL BAKAL (RAW STOCK)",
        "sec_proc": "2. JAM MESIN PRODUKSI",
        "sec_harden": "3. PROCESS HEAT TREATMENT (HARDENING)",
        "mat_type": "Pilih Material Spec",
        "raw_weight": "Berat Part (kg)",
        "mat_price": "Harga Raw Mat. / kg (Rp)",
        "waste": "Waste Material (%)",
        "lathe_hrs": "Jam Mesin Bubut",
        "mill_hrs": "Jam Mesin Milling",
        "surf_grind_hrs": "Jam Surface Grinding",
        "cyl_grind_hrs": "Jam Cylindrical Grinding",
        "tooling_cost": "Estimasi Insert & Consumable (Rp)",
        "notes": "Catatan Instruksi Kerja & Toleransi Presisi",
        "summary_title": "📊 COST BREAKDOWN & COMMERCIAL QUOTATION",
        "total_mat": "Total Material",
        "total_proc": "Total Jam Mesin",
        "total_harden": "Biaya Hardening",
        "hpp": "HPP Produksi (COGS)",
        "quote_price": "ESTIMASI HARGA PENAWARAN (COMMERCIAL QUOTE)",
        "outer_d": "Dia. Stock OD (mm)",
        "finish_d": "Dia. Finish OD (mm)",
        "length": "Panjang Cutting L (mm)",
        "depth": "Depth / Pass (mm)",
        "feed": "Feed Rate (mm/rev)",
        "cutter_d": "Dia. Cutter (mm)",
        "flutes": "Mata Potong (Z)",
        "feed_tooth": "Feed/Tooth (mm/z)",
        "enable_harden": "Tambahkan Proses Hardening (Sepuh)",
        "warn_ss400": "🚫 SS400 / Mild Steel TIDAK BISA di-harden langsung! (Kadar Karbon C < 0.25%)",
        "target_hrc": "Target Hardness Spec",
        "mach_type": "Tipe Mesin"
    },
    "EN": {
        "title": "⚙️ MACHINING & HEAT TREATMENT COST ESTIMATOR",
        "subtitle": "SYSTEM COST CALCULATOR & CYCLE TIME ANALYZER — POWERED FOR BANG BOY",
        "setting_rates": "🛠️ MACHINE & LABOR RATES",
        "rate_bubut_man": "Manual Lathe Rate (IDR/Hr)",
        "rate_bubut_cnc": "CNC Lathe Rate (IDR/Hr)",
        "rate_mill_man": "Manual Milling Rate (IDR/Hr)",
        "rate_mill_cnc": "CNC Milling Rate (IDR/Hr)",
        "rate_surf_grind": "Surface Grinding (IDR/Hr)",
        "rate_cyl_grind": "Cylindrical Grinding (IDR/Hr)",
        "rate_hardening": "Hardening Rate (IDR/kg)",
        "min_hardening": "Min. Hardening Charge (IDR)",
        "margin": "Target Profit Margin (%)",
        "doc_title": "📷 WORKPIECE DRAWING / PHOTO",
        "img_source": "Image Source:",
        "cam_opt": "Live Camera",
        "upload_opt": "Upload CAD/Photo",
        "cam_label": "Capture Workpiece Photo",
        "calc_title": "🧮 AUTOMATIC CYCLE TIME CALCULATOR",
        "tab_lathe": "🌀 Turning",
        "tab_mill": "🔲 Milling",
        "tab_s_grind": "⬛ Surface Grinding",
        "tab_c_grind": "⭕ Cylindrical Grinding",
        "form_title": "📋 COSTING & SPECIFICATIONS",
        "sec_mat": "1. RAW STOCK MATERIAL",
        "sec_proc": "2. MACHINING ALLOCATION",
        "sec_harden": "3. HEAT TREATMENT PROCESS",
        "mat_type": "Select Material Spec",
        "raw_weight": "Stock Weight (kg)",
        "mat_price": "Material Cost / kg (IDR)",
        "waste": "Waste Factor (%)",
        "lathe_hrs": "Lathe Machine (Hrs)",
        "mill_hrs": "Milling Machine (Hrs)",
        "surf_grind_hrs": "Surface Grinder (Hrs)",
        "cyl_grind_hrs": "Cylindrical Grinder (Hrs)",
        "tooling_cost": "Tooling & Inserts Cost (IDR)",
        "notes": "Job Notes & Precision Tolerances",
        "summary_title": "📊 COST BREAKDOWN & COMMERCIAL QUOTATION",
        "total_mat": "Material Cost",
        "total_proc": "Machining Cost",
        "total_harden": "Hardening Cost",
        "hpp": "Total COGS (HPP)",
        "quote_price": "RECOMMENDED COMMERCIAL QUOTE",
        "outer_d": "Stock Dia. OD (mm)",
        "finish_d": "Finish Dia. OD (mm)",
        "length": "Length L (mm)",
        "depth": "Depth / Pass (mm)",
        "feed": "Feed Rate (mm/rev)",
        "cutter_d": "Cutter Dia. (mm)",
        "flutes": "Flutes (Z)",
        "feed_tooth": "Feed/Tooth (mm/z)",
        "enable_harden": "Include Hardening Process",
        "warn_ss400": "🚫 SS400 / Mild Steel CANNOT be direct hardened! (Low Carbon Content C < 0.25%)",
        "target_hrc": "Target Hardness Spec",
        "mach_type": "Machine Type"
    }
}

# --- SIDEBAR CONTROL ---
language = st.sidebar.selectbox("🌐 UI Language / Bahasa", ["Bahasa Indonesia", "English"])
L = LANG["ID"] if language == "Bahasa Indonesia" else LANG["EN"]

st.sidebar.markdown("---")
st.sidebar.header(L["setting_rates"])
rate_bubut_man = st.sidebar.number_input(L["rate_bubut_man"], value=120000, step=10000)
rate_bubut_cnc = st.sidebar.number_input(L["rate_bubut_cnc"], value=180000, step=10000)
rate_mill_man = st.sidebar.number_input(L["rate_mill_man"], value=140000, step=10000)
rate_mill_cnc = st.sidebar.number_input(L["rate_mill_cnc"], value=220000, step=10000)
rate_surf_grind = st.sidebar.number_input(L["rate_surf_grind"], value=160000, step=10000)
rate_cyl_grind = st.sidebar.number_input(L["rate_cyl_grind"], value=180000, step=10000)

st.sidebar.markdown("---")
st.sidebar.subheader("🔥 Heat Treatment Setup")
rate_harden_per_kg = st.sidebar.number_input(L["rate_hardening"], value=25000, step=2500)
min_charge_harden = st.sidebar.number_input(L["min_hardening"], value=150000, step=25000)

st.sidebar.markdown("---")
margin = st.sidebar.slider(L["margin"], min_value=10, max_value=60, value=25)

PRESET_MAT = {
    "SS400 / Mild Steel": {"vc": 100, "can_harden": False},
    "S45C / Carbon Steel": {"vc": 120, "can_harden": True},
    "SS304 / Stainless Steel": {"vc": 80, "can_harden": False},
    "SKD61 / Tool Steel": {"vc": 70, "can_harden": True},
    "SKD11 / Cold Work Steel": {"vc": 60, "can_harden": True},
    "Cast Iron (FC 25)": {"vc": 100, "can_harden": False},
    "Bronze / Brass": {"vc": 180, "can_harden": False}
}

# --- MAIN HEADER BANNER ---
st.markdown(f"""
<div class="eng-header">
    <div class="eng-title">{L['title']}</div>
    <div class="eng-subtitle">{L['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

# --- KOLOM KIRI ---
with col_left:
    st.markdown(f"<div class='section-header'>{L['doc_title']}</div>", unsafe_allow_html=True)
    metode_gambar = st.radio(L["img_source"], [L["cam_opt"], L["upload_opt"]], horizontal=True)
    
    if metode_gambar == L["cam_opt"]:
        st.camera_input(L["cam_label"])
    else:
        uploaded_img = st.file_uploader("Upload Foto Part / Drawing", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            st.image(Image.open(uploaded_img), use_container_width=True)

    st.markdown(f"<div class='section-header'>{L['calc_title']}</div>", unsafe_allow_html=True)
    
    tab_b, tab_m, tab_sg, tab_cg = st.tabs([L["tab_lathe"], L["tab_mill"], L["tab_s_grind"], L["tab_c_grind"]])

    # 1. BUBUT
    with tab_b:
        tipe_bubut = st.radio(f"{L['mach_type']} Bubut:", ["Bubut Manual", "Bubut CNC"], horizontal=True, key="tb_type")
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            d_bakal = st.number_input(L["outer_d"], value=50.0, step=5.0)
            d_jadi = st.number_input(L["finish_d"], value=40.0, step=5.0)
            panjang_bubut = st.number_input(L["length"], value=100.0, step=10.0)
        with c_b2:
            depth_pass_b = st.number_input(L["depth"], value=1.5, step=0.5, key="db")
            feed_b = st.number_input(L["feed"], value=0.2, step=0.05, key="fb")
            mat_b = st.selectbox(L["mat_type"], list(PRESET_MAT.keys()), key="mb")

        vc_b = PRESET_MAT[mat_b]["vc"] * (1.3 if "CNC" in tipe_bubut else 1.0)
        rpm_b = (vc_b * 1000) / (math.pi * d_bakal) if d_bakal > 0 else 0
        total_depth_b = (d_bakal - d_jadi) / 2.0
        num_pass_b = math.ceil(total_depth_b / depth_pass_b) if total_depth_b > 0 else 1
        
        setup_time_b = 25 if "CNC" in tipe_bubut else 10  # setup CNC lebih lama (programming/setting tooling)
        menit_bubut = ((panjang_bubut * num_pass_b) / (feed_b * rpm_b)) if (rpm_b > 0 and feed_b > 0) else 0

    # 2. MILLING
    with tab_m:
        tipe_milling = st.radio(f"{L['mach_type']} Milling:", ["Milling Manual", "Milling CNC / VMC"], horizontal=True, key="tm_type")
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            panjang_mill = st.number_input(L["length"], value=150.0, step=10.0, key="mlen")
            lebar_mill = st.number_input("Lebar W (mm)", value=80.0, step=10.0, key="mwid")
            dalam_mill = st.number_input(L["depth"], value=5.0, step=1.0, key="mdep")
        with c_m2:
            d_cutter = st.number_input(L["cutter_d"], value=16.0, step=2.0)
            z_flute = st.number_input(L["flutes"], value=4, step=1)
            f_per_tooth = st.number_input(L["feed_tooth"], value=0.05, step=0.01)
            mat_m = st.selectbox(L["mat_type"], list(PRESET_MAT.keys()), key="mm")

        vc_m = PRESET_MAT[mat_m]["vc"] * (1.4 if "CNC" in tipe_milling else 1.0)
        rpm_m = (vc_m * 1000) / (math.pi * d_cutter) if d_cutter > 0 else 0
        feed_table = f_per_tooth * z_flute * rpm_m
        step_over = d_cutter * 0.6
        num_pass_w = math.ceil(lebar_mill / step_over) if step_over > 0 else 1
        num_pass_h = math.ceil(dalam_mill / 2.0) if dalam_mill > 0 else 1
        
        setup_time_m = 30 if "CNC" in tipe_milling else 15
        menit_milling = ((panjang_mill * num_pass_w * num_pass_h) / feed_table) if feed_table > 0 else 0

    # 3. SURFACE GRINDING
    with tab_sg:
        c_sg1, c_sg2 = st.columns(2)
        with c_sg1:
            l_sg = st.number_input("Panjang Flat (mm)", value=200.0, step=10.0, key="lsg")
            w_sg = st.number_input("Lebar Flat (mm)", value=100.0, step=10.0, key="wsg")
        with c_sg2:
            stock_sg = st.number_input("Stok Pemakanan (mm)", value=0.3, step=0.05, key="stsg")
            pass_depth_sg = st.number_input("Infeed per Pass (mm)", value=0.01, step=0.005, key="pdsg")
        
        passes_sg = math.ceil(stock_sg / pass_depth_sg) if pass_depth_sg > 0 else 1
        menit_surf_grind = (passes_sg * 0.5) + ((l_sg * w_sg) / 10000)

    # 4. CYLINDRICAL GRINDING
    with tab_cg:
        c_cg1, c_cg2 = st.columns(2)
        with c_cg1:
            d_cg = st.number_input("Dia. Grinding (mm)", value=40.0, step=5.0, key="dcg")
            l_cg = st.number_input("Panjang Shaft (mm)", value=150.0, step=10.0, key="lcg")
        with c_cg2:
            stock_cg = st.number_input("Stok Pemakanan (mm)", value=0.25, step=0.05, key="stcg")
            pass_depth_cg = st.number_input("Infeed per Pass (mm)", value=0.005, step=0.001, key="pdcg")

        passes_cg = math.ceil(stock_cg / pass_depth_cg) if pass_depth_cg > 0 else 1
        menit_cyl_grind = (passes_cg * 0.8) + ((math.pi * d_cg * l_cg) / 15000)

    jam_bubut_auto = (menit_bubut + setup_time_b) / 60 if menit_bubut > 0 else 0
    jam_milling_auto = (menit_milling + setup_time_m) / 60 if menit_milling > 0 else 0
    jam_sg_auto = (menit_surf_grind + 10) / 60 if menit_surf_grind > 0 else 0
    jam_cg_auto = (menit_cyl_grind + 15) / 60 if menit_cyl_grind > 0 else 0

# --- KOLOM KANAN ---
with col_right:
    st.markdown(f"<div class='section-header'>{L['form_title']}</div>", unsafe_allow_html=True)
    
    st.subheader(L["sec_mat"])
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        material = st.selectbox(L["mat_type"], list(PRESET_MAT.keys()), key="mat_final")
        berat_kg = st.number_input(L["raw_weight"], value=5.0, step=0.5)
    with col_m2:
        harga_per_kg = st.number_input(L["mat_price"], value=30000, step=1000)
        waste_factor = st.slider(L["waste"], min_value=0, max_value=30, value=10)

    st.subheader(L["sec_proc"])
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        jam_bubut = st.number_input(f"{L['lathe_hrs']} ({tipe_bubut})", value=float(f"{jam_bubut_auto:.2f}"), step=0.25)
        jam_surf_grind = st.number_input(L["surf_grind_hrs"], value=float(f"{jam_sg_auto:.2f}"), step=0.25)
    with c_p2:
        jam_milling = st.number_input(f"{L['mill_hrs']} ({tipe_milling})", value=float(f"{jam_milling_auto:.2f}"), step=0.25)
        jam_cyl_grind = st.number_input(L["cyl_grind_hrs"], value=float(f"{jam_cg_auto:.2f}"), step=0.25)

    biaya_tooling = st.number_input(L["tooling_cost"], value=45000, step=5000)

    st.subheader(L["sec_harden"])
    can_harden_flag = PRESET_MAT[material]["can_harden"]
    
    if not can_harden_flag:
        st.error(L["warn_ss400"])
        do_harden = False
        biaya_hardening = 0.0
    else:
        do_harden = st.checkbox(L["enable_harden"], value=True)
        if do_harden:
            c_h1, c_h2 = st.columns(2)
            with c_h1:
                target_hrc = st.text_input(L["target_hrc"], value="58 - 60 HRC")
            with c_h2:
                qty_pcs = st.number_input("Jumlah Order (Pcs)", value=1, step=1)
            
            total_berat_harden = berat_kg * qty_pcs
            hitung_biaya_harden = total_berat_harden * rate_harden_per_kg
            biaya_hardening = max(hitung_biaya_harden, min_charge_harden)
            st.info(f"🔥 Hardening Subtotal: **Rp {biaya_hardening:,.0f}** (Basis {total_berat_harden:.1f} kg)")
        else:
            biaya_hardening = 0.0

    catatan_job = st.text_area(L["notes"], f"Proses: {tipe_bubut}, {tipe_milling}, Hardening, Grinding.")

# --- RINGKASAN & BANNER HARGA ---
selected_rate_bubut = rate_bubut_cnc if "CNC" in tipe_bubut else rate_bubut_man
selected_rate_milling = rate_mill_cnc if "CNC" in tipe_milling else rate_mill_man

total_biaya_mat = (berat_kg * harga_per_kg) * (1 + (waste_factor / 100))
total_biaya_proses = (jam_bubut * selected_rate_bubut) + (jam_milling * selected_rate_milling) + (jam_surf_grind * rate_surf_grind) + (jam_cyl_grind * rate_cyl_grind)
hpp = total_biaya_mat + total_biaya_proses + biaya_tooling + biaya_hardening
harga_penawaran = hpp * (1 + (margin / 100))

st.markdown("---")
st.markdown(f"<div class='section-header'>{L['summary_title']}</div>", unsafe_allow_html=True)

col_r1, col_r2, col_r3, col_r4 = st.columns(4)

with col_r1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{L['total_mat']}</div>
        <div class="metric-value">Rp {total_biaya_mat:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_r2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{L['total_proc']}</div>
        <div class="metric-value">Rp {total_biaya_proses:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_r3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{L['total_harden']}</div>
        <div class="metric-value">Rp {biaya_hardening:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_r4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{L['hpp']}</div>
        <div class="metric-value">Rp {hpp:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# COMMERCIAL QUOTE BANNER
st.markdown(f"""
<div class="quote-banner">
    <div style="font-size: 13px; letter-spacing: 1.5px; font-weight: 700; text-transform: uppercase;">{L['quote_price']}</div>
    <div class="quote-price">Rp {harga_penawaran:,.0f}</div>
    <div style="font-size: 13px; opacity: 0.9; margin-top: 6px;">Margin Profit Target: {margin}%</div>
</div>
""", unsafe_allow_html=True)
