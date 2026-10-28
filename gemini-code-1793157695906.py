import streamlit as st
import pandas as pd
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="สมุดโทรศัพท์ ส.พัน.3 พล.ร.3 ปี 70",
    page_icon="📞",
    layout="centered"
)

# ตกแต่ง CSS เพิ่มเติมเพื่อให้รองรับมือถือและดูสวยงาม
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 0px;
        font-size: 24px;
    }
    .sub-title {
        text-align: center;
        color: #4B5563;
        margin-bottom: 20px;
        font-size: 16px;
    }
    .contact-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #1E3A8A;
        border-radius: 8px;
        padding: 12px 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)

# แสดงโลโก้ปกสมุดโทรศัพท์
try:
    image = Image.open('149343.jpg')
    st.image(image, use_container_width=True)
except Exception:
    st.warning("ไม่พบไฟล์รูปภาพโลโก้ '149343.jpg' กรุณาตรวจสอบชื่อไฟล์ในโฟลเดอร์")

st.markdown("<h1 class='main-title'>สมุดโทรศัพท์กำลังพล ส.พัน.3 พล.ร.3 ปี 70</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>กองสัญญาณที่ 3 กองพลทหารราบที่ 3</p>", unsafe_allow_html=True)

# โหลดข้อมูลจากไฟล์ contacts.csv
@st.cache_data
def load_data():
    return pd.read_csv('contacts.csv', dtype=str)

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ ไม่พบไฟล์ contacts.csv กรุณาสสร้างไฟล์ CSV สำหรับเก็บข้อมูลรายชื่อก่อนใช้งาน")
    st.stop()

# ช่องค้นหาแบบเรียลไทม์
search_query = st.text_input("🔍 ค้นหา (พิมพ์ชื่อ, นามสกุล, ตำแหน่ง, นามเรียกขาน หรือเบอร์โทร)", "")

# กรองข้อมูลตามคำค้นหา
if search_query:
    query = search_query.lower()
    mask = (
        df['FirstName'].str.lower().str.contains(query, na=False) |
        df['Last Name'].str.lower().str.contains(query, na=False) |
        df['Job Title'].str.lower().str.contains(query, na=False) |
        df['Mobile Phone'].str.lower().str.contains(query, na=False) |
        df['Notes'].str.lower().str.contains(query, na=False)
    )
    filtered_df = df[mask]
else:
    filtered_df = df

st.markdown(f"<p style='color: #64748b; font-size: 14px;'><b>กำลังพลทั้งหมดในระบบ:</b> {len(filtered_df)} นาย</p>", unsafe_allow_html=True)

# แสดงผลรายชื่อในรูปแบบ Card พร้อมปุ่มโทรออก (tel:)
for index, row in filtered_df.iterrows():
    first_name = row.get('FirstName', '')
    last_name = row.get('Last Name', '')
    job_title = row.get('Job Title', '')
    phone = row.get('Mobile Phone', '')
    notes = row.get('Notes', '')
    
    st.markdown(f"""
        <div class="contact-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 16px; font-weight: bold; color: #1e293b;">{first_name} {last_name}</div>
                    <div style="margin-top: 2px; color: #475569; font-size: 13px;"><b>ตำแหน่ง:</b> {job_title}</div>
                    <div style="margin-top: 2px; color: #0284c7; font-size: 13px;"><b>นามเรียกขาน:</b> {notes}</div>
                    <div style="margin-top: 2px; color: #334155; font-size: 13px;"><b>เบอร์โทร:</b> {phone}</div>
                </div>
                <div>
                    <a href="tel:{phone}" style="background-color: #16a34a; color: white; padding: 8px 14px; border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block; font-size: 13px; white-space: nowrap;">📞 โทรออก</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)