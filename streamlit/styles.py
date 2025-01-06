import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        /* Thiết lập chiều rộng cho sidebar khi mở */
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 350px;
            background-color: #ffffff;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
            transition: margin-left 0.2s ease;
        }

        /* Thiết lập chiều rộng cho sidebar khi đóng */
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 350px;
            margin-left: -350px;
            transition: margin-left 0.2s ease;
        }

        /* Định dạng tiêu đề */
        .sidebar-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }

        /* Định dạng tiêu đề phụ */
        .sidebar-subheader {
            font-size: 20px;
            color: #666;
        }

        /* Định dạng dropdown */
        .stSelectbox {
            background-color: #ffffff;
            color: #333;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 10px;
            transition: border-color 0.3s;
        }

        /* Định dạng khi hover lên dropdown */
        .stSelectbox:hover {
            border-color: #2E7D32;
        }

        /* Định dạng bảng thành viên */
        .member-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .member-table th, .member-table td {
            border: 1px solid #4CAF50;
            padding: 12px;
            text-align: center;
            transition: background-color 0.3s;
            width: 33.33%; /* Chiều rộng cố định cho các cột */
        }
        .member-table th {
            background-color: #4CAF50;
            color: white;
        }
        .member-table tr:hover {
            background-color: rgba(76, 175, 80, 0.1);
        }

        /* Định dạng hình ảnh */
        .image-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }

        img {
            width: 300px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
