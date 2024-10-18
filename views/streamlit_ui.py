import streamlit as st
import pandas as pd
from controller.question_controller import QuestionController
from controller.cot_controller import CoTController
from controller.rag_controller import RAGController 
from src.model import EmbeddingModel
from datetime import date, datetime

def inject_custom_css():
    st.markdown("""
    <style>
        body {
            font-family: 'Georgia', serif;
        }
        .custom-input {
            padding: 15px;
            font-size: 16px;
            border: 1px solid #007bff;
            border-radius: 25px;
            background-color: #f8f9fa;
            font-family: 'Georgia', serif;
            box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .send-button {
            background-color: #007bff;
            border: none;
            color: white;
            padding: 12px 18px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        .send-button:hover {
            background-color: #0056b3;
        }
    </style>
    """, unsafe_allow_html=True)

# Khởi tạo controller và mô hình
controller = QuestionController()
cot_controller = CoTController()
rag_controller = RAGController()
embedding_model = EmbeddingModel()

# Tải danh mục từ CSV
def load_categories():
    df = pd.read_csv('/Users/datarist/EconVNNewsBot/controller/categories.csv')
    categories = df['category'].tolist()
    categories.insert(0, "Tất cả")
    return categories

# Tải nguồn từ CSV
def load_sources():
    df = pd.read_csv('/Users/datarist/EconVNNewsBot/controller/source.csv')
    sources = df['source'].tolist()
    sources.insert(0, "Tất cả")
    return sources

if 'query_history' not in st.session_state:
    st.session_state['query_history'] = []

def add_query_to_history(query):
    """Thêm truy vấn vào lịch sử truy vấn"""
    if query not in st.session_state['query_history']:
        st.session_state['query_history'].append(query)

def convert_string_to_date(date_str):
    """Chuyển đổi chuỗi 'yyyy-mm-dd' sang đối tượng datetime.date"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None  # Trả về None nếu ngày không hợp lệ hoặc không thể phân tích

def display_query_ui():
    inject_custom_css()

    # Sidebar - Tùy chọn Lọc và Lịch sử Truy vấn
    with st.sidebar:
        st.subheader("Tùy chọn Lọc")
        selected_category = st.selectbox("Lọc theo Danh mục", load_categories(), key="category_select")
        selected_source = st.selectbox("Lọc theo Nguồn", load_sources(), key="source_select")
        
        # Lọc theo ngày xuất bản (dạng yyyy-mm-dd)
        st.subheader("Lọc theo Ngày xuất bản")
        start_date = st.date_input("Ngày bắt đầu", date(2020, 1, 1))  # Ngày bắt đầu mặc định
        end_date = st.date_input("Ngày kết thúc", date.today())  # Ngày kết thúc mặc định là hôm nay
        
        if start_date > end_date:
            st.warning("Ngày bắt đầu phải nhỏ hơn ngày kết thúc!")

        st.subheader("Lịch sử Truy vấn")
        st.markdown("Dưới đây là các truy vấn gần đây của bạn. Nhấp để chạy lại chúng.")
        # Lịch sử Truy vấn
        if st.session_state['query_history']:
            selected_history = st.selectbox("Truy vấn trước đây:", st.session_state['query_history'], key='history_select')
            st.session_state['user_query'] = selected_history

    # Khởi tạo user_query trong session state nếu chưa có
    if 'user_query' not in st.session_state:
        st.session_state['user_query'] = ""

    # Xử lý truy vấn trước và hiển thị kết quả trên hộp nhập liệu
    if 'generated_answer' in st.session_state:
        st.markdown('<h4 style="color: #1a7d3b;">Câu hỏi:</h4>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 18px; font-family: Georgia, serif; text-align: justify;">{st.session_state["user_query"]}</p>', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1a7d3b;">Câu trả lời là:</h4>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size: 18px; font-family: Georgia, serif; text-align: justify;">{st.session_state["generated_answer"]}</p>', unsafe_allow_html=True)

        # Hiển thị nguồn tham khảo nếu có
        if 'cite_list' in st.session_state and st.session_state['cite_list']:
            st.markdown('<h4 style="color: #1a7d3b;">Nguồn tham khảo</h4>', unsafe_allow_html=True)
            for idx, article in enumerate(st.session_state['cite_list'], start=1):
                st.markdown(f'<p style="font-size: 16px;">[{idx}] {article["title"]}. Xuất bản vào {article["published_date"]}. Xem tại: <a href="{article["url"]}">{article["url"]}</a></p>', unsafe_allow_html=True)

    # Tạo hai cột: một cho hộp nhập liệu và một cho nút bấm
    col1, col2 = st.columns([5, 1])  # Cột 1 (nhập liệu) rộng hơn, Cột 2 (nút bấm) hẹp hơn

    with col1:
        user_query = st.text_input("", value=st.session_state['user_query'], key="user_query_input", placeholder="Nhập câu hỏi của bạn...", label_visibility='collapsed')

    with col2:
        send_button = st.button("⤴️", key='submit_button', help='Gửi Truy vấn')

    # Xử lý truy vấn khi nút bấm được nhấn
    if send_button and user_query:
        st.session_state['user_query'] = user_query  # Cập nhật session state
        add_query_to_history(user_query)  # Thêm vào lịch sử

        try:
            # Chuyển đổi truy vấn thành vector
            input_vector = embedding_model.embed_text(user_query).flatten().tolist()

            # Xây dựng từ điển lọc
            filter_dict = {}
            if selected_category != "Tất cả":
                filter_dict["category"] = {"$eq": selected_category}
            if selected_source != "Tất cả":
                filter_dict["source"] = {"$eq": selected_source}

            # Truy vấn Pinecone để lấy các kết quả phù hợp nhất
            top_k_vectors = controller.query_by_vector(input_vector, top_k=15, filter=filter_dict)

            # Thu thập các bài viết liên quan và lọc theo khoảng ngày xuất bản
            related_articles = []
            for match in top_k_vectors:
                article_date = convert_string_to_date(match["metadata"].get("published_date", "N/A"))

                # Chỉ bao gồm các bài viết trong khoảng ngày đã chọn
                if article_date and start_date <= article_date <= end_date:
                    article = {
                        "title": match["metadata"].get("title", "N/A"),
                        "url": match["metadata"].get("url", "N/A"),
                        "content": match["metadata"].get("content", "N/A"),
                        "published_date": match["metadata"].get("published_date", "N/A")
                    }
                    related_articles.append(article)

            # **Rerank the articles using RAGController**
            if related_articles:
                reranked_articles = rag_controller.rerank_articles(user_query, related_articles, top_k=5)
                
                # Sinh Chuỗi Suy Nghĩ (CoT)
                final_answer, cite_list = cot_controller.generate_chain_of_thoughts(reranked_articles, user_query)
                
                st.session_state['generated_answer'] = final_answer  # Lưu câu trả lời vào session state
                st.session_state['cite_list'] = cite_list  # Lưu danh sách nguồn tham khảo

        except Exception as e:
            st.error(f"Lỗi: {str(e)}")

    elif send_button and not user_query:
        st.warning("Vui lòng nhập câu hỏi.")