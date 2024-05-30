import streamlit as st
from utils import load_context_data
from model import get_response
import os
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def main():
    st.title('Vidya')
    st.subheader('Your Educational Companion')

    # Load context data
    context_data = load_context_data('data')

    user_input = st.text_input("Ask your Query")

    st.write("Upload your competitive exam result (optional):")
    uploaded_result_report = st.file_uploader("", type=['pdf'])

    if st.button('Get Response'):
        if user_input or uploaded_result_report:
            try:
                if uploaded_result_report:
                    result_report_path = os.path.join("uploads", uploaded_result_report.name)
                    with open(result_report_path, "wb") as f:
                        f.write(uploaded_result_report.getbuffer())
                else:
                    result_report_path = None

                response = get_response(user_input, context_data, result_report_path, API_KEY)
                if response:
                    st.success("Response received!")
                    st.write(response)
                else:
                    st.error("No relevant information found.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)} - {type(e).__name__}")
        else:
            st.error("Please enter a query or upload a result report to get a response.")

if __name__ == "__main__":
    main()
