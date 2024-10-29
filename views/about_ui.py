import streamlit as st

# Hàm hiển thị trang "Giới thiệu"
def display_about_ui():
    st.title("Giới thiệu về EconVNNewsBot")

    st.header("Giới thiệu")
    st.write("""
    **EconVNNewsBot** là một hệ thống sử dụng AI, được thiết kế để truy vấn và truy xuất tin tức kinh tế Việt Nam một cách hiệu quả.
    Hệ thống kết hợp các mô hình AI tiên tiến và kỹ thuật **Dựa Trên Truy Xuất Thông Tin (RAG)** cùng với **Chuỗi Suy Nghĩ (CoT)** để 
    cung cấp câu trả lời chính xác và dựa trên ngữ cảnh thông qua việc phân tích và tổng hợp nội dung tin tức liên quan.
    """)

    st.header("Quy trình hệ thống")
    st.image("docs/EconVNNewsBot.png", caption="Quy trình hoạt động của hệ thống EconVNNewsBot")

    st.write("""
    Quy trình hoạt động của **EconVNNewsBot** đảm bảo rằng người dùng nhận được câu trả lời chính xác và có tính lý luận. Dưới đây là cái nhìn tổng quan về quy trình:

    1. **Thu thập dữ liệu**: 
       - Các bài báo tin tức được thu thập từ nhiều nguồn tin kinh tế Việt Nam khác nhau qua mô-đun **EconVNNewsCrawl**.
       - Những bài báo này được lưu trữ trong một cơ sở dữ liệu tập trung để phục vụ cho việc phân tích.

    2. **Phân đoạn ngữ nghĩa**:
       - Các bài báo dài được chia thành các đoạn ngữ nghĩa nhỏ hơn, giúp truy xuất chính xác và đảm bảo rằng mỗi đoạn đều liên quan đến truy vấn của người dùng.

    3. **Nhúng văn bản**:
       - Các đoạn văn bản được chuyển đổi thành các biểu diễn vector thông qua **Mô hình nhúng văn bản (jina-embeddings-v3)** và lưu trữ trong **Cơ sở dữ liệu vector** để tìm kiếm nhanh chóng.

    4. **Xử lý truy vấn**:
       - Các truy vấn của người dùng cũng được chuyển đổi thành vector sử dụng **Mô hình nhúng câu hỏi**, để dễ dàng so sánh với dữ liệu đã lưu.

    5. **Tìm kiếm và truy xuất vector**:
       - Hệ thống tìm kiếm trong **Cơ sở dữ liệu vector** để xác định và xếp hạng những nội dung có độ tương đồng cao nhất với truy vấn.

    6. **Chuỗi Suy Nghĩ (CoT)**:
       - Các kết quả hàng đầu được phân tích và tổng hợp qua mô-đun **Chuỗi Suy Nghĩ (CoT)**, kết hợp thông tin từ nhiều nguồn để tạo ra câu trả lời mạch lạc và đầy đủ.

    7. **Sinh câu trả lời**:
       - Câu trả lời cuối cùng được tạo ra, dựa trên thông tin từ nhiều bài viết, cùng với các nguồn tham khảo để tăng tính minh bạch và độ tin cậy.
    """)

    st.header("Tính năng chính")
    st.write("""
    - **EconVNNewsCrawl**: Crawler web tùy chỉnh để thu thập tin tức kinh tế Việt Nam từ các nguồn đáng tin cậy.
    - **Phân đoạn ngữ nghĩa**: Chia nhỏ các bài báo dài thành các đoạn có ý nghĩa để cải thiện hiệu quả truy xuất.
    - **Cơ sở dữ liệu vector**: Sử dụng Pinecone cho tìm kiếm và truy xuất vector một cách hiệu quả.
    - **Chuỗi Suy Nghĩ (CoT)**: Tổng hợp thông tin từ nhiều bài báo để đưa ra các câu trả lời chi tiết và có căn cứ.
    """)

    st.header("Đội ngũ dự án")
    st.write("""
    **EconVNNewsBot** được phát triển bởi một nhóm kỹ sư AI và các chuyên gia trong lĩnh vực kinh tế:
    - **Lê Nguyễn Đăng Khoa**
    - **Trần Tuyết Huê** 
    - **Phạm Minh Châu** 
    """)

    st.header("Thông tin liên hệ")
    st.write("""
    Mọi thắc mắc hoặc đóng góp ý kiến, vui lòng liên hệ chúng tôi qua:
    - **Email**: khoale.aius@gmail.com.vn
    - **Điện thoại**: +84 903 696 581
    """)
