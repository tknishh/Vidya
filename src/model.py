import openai
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF file.
    """
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
    return text

def get_response(user_input, context_data, result_report_path, api_key):
    """
    Generate a response based on user input, context data, and optionally the result report.

    Parameters:
    user_input (str): The user's query or input.
    context_data (str): The context data loaded from files.
    result_report_path (str): The path to the uploaded result report, if any.
    api_key (str): The API key for the OpenAI GPT model.

    Returns:
    str: The generated response.
    """
    openai.api_key = api_key

    # Extract text from the result report if provided
    result_report_text = ""
    if result_report_path:
        result_report_text = extract_text_from_pdf(result_report_path)

    # Combine user input, context data, and result report text
    combined_text = f"Context: {context_data}\n\nResult Report: {result_report_text}\n\nUser Input: {user_input}\n\n"
    
    # Ensure the combined text does not exceed context length limits
    max_context_length = 4096  # Adjust as per the model's limit
    if len(combined_text) > max_context_length:
        excess_length = len(combined_text) - max_context_length
        context_data = context_data[:-excess_length]
        combined_text = f"Context: {context_data}\n\nResult Report: {result_report_text}\n\nUser Input: {user_input}\n\n"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps a user by providing them best educational suggestions."},
                {"role": "user", "content": combined_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None
