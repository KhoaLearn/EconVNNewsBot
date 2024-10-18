import streamlit as st
from views.streamlit_ui import display_query_ui  # Cho trang tìm kiếm
from views.about_ui import display_about_ui      # Cho trang giới thiệu

# CSS tùy chỉnh để cải thiện giao diện và đồng bộ font chữ
def inject_custom_css():
    st.markdown("""
    <style>
        /* Tùy chỉnh màu nền sidebar và font chữ */
        body {
            font-family: 'Georgia', serif; /* Đặt font chữ mặc định là Georgia */
        }
        .stSidebar {
            background-color: #ccd9e6;
            font-size: 18px;
            color: #1a7d3b;
        }
        /* Tùy chỉnh nút bấm cho đẹp mắt hơn */
        .stButton > button {
            background-color: #4a8c6c;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-family: 'Georgia', serif;  /* Đồng bộ font chữ */
        }
        /* Tùy chỉnh phần header */
        .header {
            font-family: 'Georgia', serif;
            color: #1a7d3b;
            text-align: center;
            padding-bottom: 12px;
        }
        /* Tùy chỉnh các tiêu đề và văn bản */
        h1, h2, h3, h4, h5, h6, p {
            font-family: 'Georgia', serif;
        }
    </style>
    """, unsafe_allow_html=True)

# Cấu hình trang
st.set_page_config(
    layout="centered", 
    page_title="EconVNNewsBot",
    page_icon="📄"
)

# Menu Sidebar cho điều hướng
def sidebar_menu():
    st.sidebar.title("Điều hướng")
    return st.sidebar.selectbox("Chọn trang", ["Tìm kiếm", "Giới thiệu"])

# Trang thông điệp chào mừng
def display_welcome_message():
    st.markdown('<h3 style="color: #1a7d3b;" class="header">EconVNNewsBot: Hệ thống suy luận dựa trên truy xuất thông tin cho trả lời câu hỏi về tin tức kinh tế Việt Nam</h3>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 18px;">Hệ thống này cung cấp các câu trả lời chính xác, dựa trên bối cảnh từ một kho tin tức kinh tế Việt Nam rộng lớn, được hỗ trợ bởi suy luận RAT và các nguồn tham khảo uy tín.</p>', unsafe_allow_html=True)

# Hàm chính của ứng dụng
def main():
    # Chèn CSS tùy chỉnh
    inject_custom_css()

    # Hiển thị thông điệp chào mừng khi khởi động
    display_welcome_message()
    
    # Điều hướng Sidebar
    selected_page = sidebar_menu()

    # Điều hướng giữa các trang dựa vào lựa chọn của người dùng
    if selected_page == "Tìm kiếm":
        display_query_ui()  
    elif selected_page == "Giới thiệu":
        display_about_ui()  

# Điểm bắt đầu chính của ứng dụng
if __name__ == "__main__":
    main()
