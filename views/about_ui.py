import streamlit as st

# Hàm hiển thị trang "Giới thiệu"
def display_about_ui():
    st.title("Giới thiệu về EconVNNewsBot")

    st.header("Giới thiệu")
    st.write("""
    EconVNNewsBot là một hệ thống sử dụng AI, được thiết kế để truy vấn và truy xuất tin tức kinh tế Việt Nam một cách hiệu quả. 
    Sử dụng các mô hình AI tiên tiến và khung suy luận Dựa Trên Truy Xuất Thông Tin (RAT), bot cung cấp các câu trả lời chính xác, dựa trên ngữ cảnh 
    thông qua việc phân tích và tổng hợp nội dung tin tức có liên quan.
    """)

    st.header("Quy trình hệ thống")
    st.image("/Users/datarist/EconVNNewsBot/docs/EconVNNewsBot.png", caption="Quy trình hoạt động của hệ thống EconVNNewsBot")

    st.write("""
    Quy trình hoạt động của EconVNNewsBot đảm bảo rằng người dùng nhận được các câu trả lời chính xác và có lý luận hợp lý. Dưới đây là cái nhìn tổng quan về quy trình:

    1. **Thu thập dữ liệu**: 
       - Các bài báo tin tức được thu thập từ nhiều nguồn tin kinh tế Việt Nam khác nhau bằng mô-đun **EconVNNewsCrawl**.
       - Các bài báo này được lưu trữ trong cơ sở dữ liệu tập trung để phân tích.

    2. **Phân đoạn ngữ nghĩa**:
       - Các bài báo được chia thành các đoạn ngữ nghĩa có ý nghĩa để truy xuất chính xác, đảm bảo rằng mỗi phần nội dung đều có liên quan đến truy vấn của người dùng.

    3. **Nhúng văn bản**:
       - Các đoạn văn bản được chuyển đổi thành các biểu diễn vector thông qua một **Mô hình nhúng văn bản** và được lưu trữ trong **Cơ sở dữ liệu vector** để tìm kiếm tương đồng nhanh chóng.

    4. **Xử lý truy vấn**:
       - Các truy vấn của người dùng được chuyển đổi thành các biểu diễn vector bằng cách sử dụng một **Mô hình nhúng câu hỏi** để so sánh hiệu quả.

    5. **Tìm kiếm & truy xuất vector**:
       - Hệ thống sẽ tìm kiếm trong **Cơ sở dữ liệu vector** để tìm và xếp hạng những nội dung liên quan nhất dựa trên độ tương đồng với truy vấn.

    6. **Suy luận Chuỗi Suy Nghĩ (CoT)**:
       - Các kết quả hàng đầu được phân tích bằng mô-đun **Chuỗi Suy Nghĩ (CoT)**, tổng hợp thông tin từ nhiều nguồn để tạo ra một câu trả lời mạch lạc và mang tính thông tin.

    7. **Sinh câu trả lời**:
       - Một câu trả lời cuối cùng được tạo ra, được hỗ trợ bởi thông tin từ nhiều bài viết và trích dẫn các nguồn tham khảo.
    """)

    st.header("Tính năng chính")
    st.write("""
    - **EconVNNewsCrawl**: Crawler web tùy chỉnh để thu thập tin tức kinh tế Việt Nam.
    - **Phân đoạn ngữ nghĩa**: Chia nhỏ các bài báo lớn để truy xuất nội dung tốt hơn.
    - **Cơ sở dữ liệu vector**: Sử dụng Pinecone để tìm kiếm và truy xuất dựa trên vector hiệu quả.
    - **Suy luận Chuỗi Suy Nghĩ**: Tổng hợp nội dung từ nhiều bài viết để đưa ra các câu trả lời rõ ràng và có căn cứ.
    """)

    st.header("Đội ngũ dự án")
    st.write("""
    EconVNNewsBot được phát triển bởi một đội ngũ gồm các kỹ sư AI và chuyên gia trong lĩnh vực:
    - **Trần Tuyết Huê** 
    - **Lê Nguyễn Đăng Khoa** 
    - **Phạm Minh Châu** - Quản lý dự án
    """)

    st.header("Thông tin liên hệ")
    st.write("""
    Mọi thắc mắc hoặc góp ý, vui lòng liên hệ chúng tôi qua:
    - **Email**: khoale.aius@gmail.com.vn
    - **Điện thoại**: +84 903 696 581
    """)
