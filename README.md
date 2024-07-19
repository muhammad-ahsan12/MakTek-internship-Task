# Chat With Website
This project is a web application that extracts text from a specified website in real-time and answers questions about the content using a
conversational AI model. It utilizes various tools including Streamlit, LangChain, BeautifulSoup, and Google Generative AI embeddings to provide accurate and context-aware responses to user queries.

# Features
Real-time Text Extraction: Extracts text from any given URL in real-time.
Conversational QA: Uses advanced conversational AI models to answer questions based on the extracted content.
User-friendly Interface: Provides a simple and intuitive interface for users to input their API key, website URL, and questions.
Persistent Vector Database: Stores text data in a Chroma vector database for efficient retrieval.
# Installation
 Clone the Repository

 [(https://github.com/muhammad-ahsan12/MakTek-internship-Task.git)](https://github.com/muhammad-ahsan12/MakTek-internship-Task.git)
# Install Dependencies
Ensure you have Python 3.8+ installed. Then install the required packages using pip:

# pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory and add your Google API key:

GOOGLE_API_KEY=your_google_api_key_here
# Usage
Run the Application

streamlit run main.py
Using the Interface

Google API Key: Enter your Google API key.
Website URL: Insert the URL of the website you want to extract text from.
Question: Type your question related to the website content.
Submit Your Query
Click the "Submit Query" button to get an answer based on the website content.

Project Structure
main.py: Main application file that sets up the Streamlit interface and handles the text extraction and QA processing.
requirements.txt: List of Python dependencies required for the project.
Example
Here's an example of how to use the application:

Enter your Google API key.
Insert the URL of a website, for example, https://example.com.
Ask a question like "What is the main topic of this page?".
Click "Submit Query" and view the answer provided by the chatbot.
Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any improvements or bug fixes.
