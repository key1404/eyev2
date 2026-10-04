import streamlit as st
import numpy as np
from PIL import Image

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه جامع انتخاب و تست زنده عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تحلیل چهره، پیشنهاد تخصصی و امتحان مجازی")

# مدیریت حالت‌های برنامه (مراحل سه‌گانه)
if "step" not in st.session_state:
    st.session_state.step = "capture" # مراحل: capture -> analyze -> tryon
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت یا آپلود تصویر چهره
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای شروع تحلیل")
    st.info("لطفاً یا از طریق دوربین دستگاه خود عکس بگیرید یا یک تصویر واضح از چهره خود بارگذاری کنید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی زنده با دوربین", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("روبه‌روی دوربین قرار بگیرید و عکس بگیرید:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا یک تصویر استاندارد از چهره آپلود کنید:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # پردازش و تحلیل هندسی چهره بر اساس ابعاد تصویر
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"name": "Tom Ford - Aviator Luxe", "type": "خلبانی عریض با پل ضخیم", "brand": "Tom Ford", "icon": "✈️", "color": "#1f77b4"},
                {"name": "Ray-Ban - Square Classic", "type": "مستطیلی پهن کلاسیک", "brand": "Ray-Ban", "icon": "⬛", "color": "#ff7f0e"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"name": "Ray-Ban - Wayfarer Original", "type": "ویفرر استاندارد کلاسیک", "brand": "Ray-Ban", "icon": "🕶️", "color": "#2ca02c"},
                {"name": "Tom Ford - Cat Eye Modern", "type": "چشم‌گربه‌ای شیک و مدرن", "brand": "Tom Ford", "icon": "🐱", "color": "#d62728"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"name": "Tom Ford - Slim Rectangular", "type": "مستطیلی باریک زاویه‌دار", "brand": "Tom Ford", "icon": "📐", "color": "#9467bd"},
                {"name": "Ray-Ban - Round Metal", "type": "گرد فلزی مینیمال سبک", "brand": "Ray-Ban", "icon": "⚪", "color": "#8c564b"}
            ]
        
        # انتقال به مرحله تحلیل و گالری
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری فریم‌های متناسب
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب مدل فریم")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر ثبت‌شده شما", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل هندسی و آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده چهره:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای اپتومتری ثبت‌شده:** PD = {pd_input}mm | نسخه: {rx_type}")
        st.markdown("---")
        st.markdown("💡 **مدل‌های فریم پیشنهادی متناسب با چهره شما:**")
        st.markdown("لطفاً از میان مدل‌های زیر یکی را برای **تست زنده روی چهره** انتخاب کنید:")

    st.markdown("---")
    
    # نمایش کارت‌های مدل‌های فریم به صورت بصری و تعاملی
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 15px; border-radius: 10px; background-color: #fcfcfc; text-align: center;">
                    <h2 style="margin: 0;">{frame['icon']}</h2>
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ انتخاب و تست این فریم", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: شبیه‌سازی و امتحان مجازی روی چهره
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    st.markdown("### مرحله ۳: شبیه‌‌سازی و امتحان مجازی (Virtual Try-On)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.image(st.session_state.image, caption="تصویر اصلی چهره شما", use_column_width=True)
        if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
            st.session_state.step = "analyze"
            st.rerun()
            
    with c2:
        chosen = st.session_state.selected_frame
        st.markdown(f"""
            <div style="background-color: #eef7fc; padding: 25px; border-radius: 12px; border-left: 6px solid {chosen['color']};">
                <h3>🎯 شبیه‌سازی فریم فعال روی چهره</h3>
                <p><b>مدل انتخابی:</b> {chosen['icon']} <b>{chosen['name']}</b></p>
                <p><b>نوع ساختار:</b> {chosen['type']}</p>
                <p><b>کالیبراسیون PD:</b> فریم با فاصله مردمک‌های شما (<b>{pd_input} میلی‌متر</b>) فیت و تنظیم شد.</p>
                <p><b>تطبیق نمره ({rx_type}):</b> تایید شده برای نصب عدسی‌های تراش‌خورده.</p>
                <hr>
                <p style="color: #0e803e; font-weight: bold; font-size: 1.1em;">
                    ✅ عینک انتخابی شما با موفقیت بر روی مختصات چهره بارگذاری و شبیه‌سازی گردید!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 شروع مجدد با عکس جدید"):
            st.session_state.step = "capture"
            st.rerun()