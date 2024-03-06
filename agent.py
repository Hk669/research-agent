import os
import json
import requests
import streamlit as st
from linkpreview import link_preview
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()
SERPER_API = os.getenv('SERPER')
OPENAI_API_KEY = os.getenv('API_KEY')

def search(query):
    """
    search the information through google
    """

    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': SERPER_API,
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()
    return response_data


def find_relevant_articles(response, query):
    """
    llm is used to find the relevant articles to the user query from response
    """
    response_data = json.dumps(response)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY,
                     model_name ='gpt-3.5-turbo',
                     temperature='0.7')
    template = """
    You are the best researcher of all time. you are extremely good at finding the relevant articles to the query;
    {response_data}
    Above is the list of search results of articles for the query: {query}.
    Please rank the best 3 articles from the list, return ONLY an array of the urls, do not include any information; 
    return ONLY an array of the urls, do not include anything else;
    """

    prompt = PromptTemplate(
        input_variables=['response_data', 'query'],
        template=template
    )

    articles_chain = LLMChain(prompt=prompt,
                              llm=llm,
                              verbose=True)
    urls = articles_chain.predict(response_data=response_data, query=query)
    print(urls)
    url_list = json.loads(urls)
    return url_list

# def scrape(article_urls):
#     """
#     scrapes the information from the article 
#     """
#     loader = UnstructuredURLLoader(urls=article_urls)
#     data = loader.load()
#     return data


def get_information_from_urls(article_urls):
    """
    Scrapes the text content from the article URLs using Selenium.
    """
    options = Options()
    options.headless = True

    # Initialize the WebDriver
    service = Service(ChromeDriverManager(driver_version='122.0.6261.112').install())
    driver = webdriver.Chrome(service=service, options=options)

    information = []

    try:
        for url in article_urls:
            try:
                driver.get(url)
                driver.implicitly_wait(10)
                text_content = driver.find_element(By.TAG_NAME, 'body').text
                information.append(text_content)
            except Exception as e:
                print(f'Error getting information {url}: {e}')
                continue
    finally:
        driver.quit()

    return information

def summarize(information):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n",],
        chunk_size=1000,
        chunk_overlap=20,
        length_function=len,
    )
    texts = text_splitter.create_documents(information)
    print(texts)
    template = """
    write a consice summary of the articles
    "{texts}"
    CONCISE SUMMARY:
    """
    prompt = PromptTemplate.from_template(template)
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Define StuffDocumentsChain
    stuff_chain = load_summarize_chain(llm=llm, chain_type="stuff")
    return stuff_chain.run(texts)

def main():
    st.title('Research Agent')
    query = st.text_input('Enter your query:')
    if st.button('Search'):
        response = search(query)
        url_list = find_relevant_articles(response, query)
        with st.expander("Articles"):
            for url in url_list:
                if url:
                    try:
                        preview = link_preview(url)
                        title = preview.title
                        description = preview.description
                        image = preview.image

                        # if image:
                        #     st.image(image, caption='Preview Image', width=100)
                        st.markdown(f'**Title:** {title}', unsafe_allow_html=True)
                        # st.markdown(f'**Description:** {description}', unsafe_allow_html=True)
                        st.markdown(f'**URL:** [{url}]({url})', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error fetching preview for URL: {url}")
                        st.error(str(e))

        data = get_information_from_urls(url_list)
        summary = summarize(data)
        st.markdown("**Answer**")
        st.write(summary)


if __name__ == '__main__':
    main()