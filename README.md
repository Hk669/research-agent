

https://github.com/Hk669/research-agent/assets/96101829/d1938a0a-9c8f-43b1-9c34-bfd137d73775

# Research Agent

The Research Agent is an AI-powered tool designed to assist users in conducting research by 
searching for information, finding relevant articles, and summarizing them automatically. This tool 
utilizes advanced natural language processing (NLP) techniques and web scraping to provide users 
with concise summaries of relevant articles on their chosen topics.


## Features

### 1. Search Functionality
Users can enter their research query into the search bar provided in the Streamlit app. The Research 
Agent then utilizes the Google SERPER API to perform a search query and retrieve relevant articles 
based on the user's input.

### 2. Article Preview
Once the search results are obtained, the Research Agent displays a list of relevant articles along 
with their titles and URLs. Additionally, it uses the Linkpreview library to fetch a preview of each 
article, including the title, description, and thumbnail image (if available), providing users with 
a quick overview of each article's content.

### 3. Summarization
After selecting an article from the list, users can click on the URL to view the full article. The 
Research Agent then uses Selenium to scrape the text content of the article from the webpage. Once 
the text content is obtained, it applies recursive character text splitting to break down the 
article into smaller chunks suitable for processing.

### 4. Automatic Summarization
Using Langchain and OpenAI's GPT-3.5 model, the Research Agent generates a concise summary of the 
rticle's content. This summary is presented to the user within the Streamlit app, allowing them to 
quickly grasp the main points of the article without having to read through the entire text.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hk669/research-agent.git
cd research-agent
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a `.env` file in the root directory and add your SERPER and OpenAI API keys:

```
SERPER=your_serper_api_key
API_KEY=your_openai_api_key
```

## Usage

1. Run the Streamlit app:

```bash
streamlit run agent.py
```

2. Enter your query in the text input field and click the "Search" button.

3. The app will display a list of relevant articles along with their titles and URLs.

4. Click on the URL to view the full article.

5. The app will generate a concise summary of the articles.

## Technologies Used

- Python
- Streamlit
- Selenium
- Langchain
- Linkpreview


## License

This project is licensed under the [MIT License](LICENSE).
