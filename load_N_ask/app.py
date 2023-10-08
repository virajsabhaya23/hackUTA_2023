from openai.error import OpenAIError
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from langchain.callbacks import get_openai_callback
from streamlit_chat import message
import os
import pandas as pd
import openai

# custom imports
from uiLayouts import *
from readFiles import *
from utils import *
from splitText import *


def ask_general_question(user_question, OPENAI_API_KEY):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_question}
        ]
    )
    answer = response['choices'][0]['message']['content']
    return answer

def create_embeddings(OPENAI_API_KEY, chunks):
    """
        Creates embeddings for each chunk
        :param OPENAI_API_KEY: OpenAI API key
        :param chunks: list of chunks
        :return: list of embeddings
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    retireved_info_knowledge = FAISS.from_texts(chunks, embeddings)
    return retireved_info_knowledge


def ask_question(user_question, chunks, OPENAI_API_KEY):
    """
        Asks a question to the model
        :param user_question: question asked by user
        :return: answer to the question
    """
    # creating embeddings
    knowledge = create_embeddings(OPENAI_API_KEY, chunks)
    docs = knowledge.similarity_search(user_question)
    llms = OpenAI(openai_api_key=OPENAI_API_KEY)
    
    qa_chain = load_qa_chain(llms, chain_type="stuff")
    response = qa_chain.run(input_documents=docs, question=user_question)

    if "I don't know" in response:  # adjust this condition based on the actual responses you get
        response = ask_general_question(user_question, OPENAI_API_KEY)
        
    return response
    

def main():
    uiHeroSection()
    # image_custom()
    # get API key from USER
    # st.write('### 1. Enter your OpenAI API key')
    # OPENAI_API_KEY = st.text_input(
    #     help="You can get your API key from https://platform.openai.com/account/api-keys",
    #     label="WARNING: API key is only free for first 3 months! check OpenAI's policy for upgraded guidelines.",
    #     type='password',
    #     placeholder="sk-abcdefghi...",
    #     # label_visibility="collapsed"
    # )
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    # get the option from user what file they are importing
    st.write('### Select the type of file you are uploading')
    file_type = st.selectbox(
        "Select the type of file you are uploading",
        ("PDF", "CSV")
    )
    
    st.write(f'### Upload your {file_type} file')
    uploaded_file = st.file_uploader(f'Upload your {file_type} files', accept_multiple_files=True)
    if uploaded_file:
        if file_type.lower().endswith('pdf'):
            text = read_pdf(uploaded_file)
            chunks = split_text(text)
            summary_question = "What is the summary of the document?" 
            summary_response = ask_question(summary_question, chunks, OPENAI_API_KEY)  
            with st.sidebar:
                st.write("## ℹ️ Summary")
                with st.expander("Details ...", expanded=True):
                    st.write(summary_response)
            init_session_state()
        elif file_type.lower().endswith('csv'):
            # csvData = pd.read_csv(uploaded_file)
            # st.dataframe(csvData, use_container_width=True)
            pass
            init_session_state()

        

        # Ask question
        st.write('### Ask your question')
        user_question = st.text_area(on_change=clear_submit, height=90, label="Ask a question about your PDF here :", placeholder="Type your question here", label_visibility="collapsed")

        button = st.button("Submit!")
        if button or st.session_state.get("submit"):
            if not uploaded_file:
                st.error("Please upload a file!")
            if not user_question:
                st.error("Please ask a question!")
            else:
                st.session_state["submit"] = True
                response = None
                try:
                    with st.spinner("Searching for answer..."):
                        if file_type.lower().endswith('pdf'):
                            response = ask_question(user_question, chunks, OPENAI_API_KEY)
                        elif file_type.lower().endswith('csv'):
                            # llm = OpenAI(api_token = OPENAI_API_KEY, temperature=0)
                            # response = df.chat(user_question)
                            ############## attempt-1 #############
                            llm = OpenAI(temperature=0)
                            agent = create_csv_agent(llm, uploaded_file, verbose=True)
                            if user_question is None : 
                                st.error("Please ask a question!")
                            else:
                                response = agent.run(user_question)
                except Exception as e:
                    st.error(e)
            #--- with get_openai_callback() as callback:
                # storing past questions and answers
            if response is not None:
                st.session_state.past.append(user_question)
                st.session_state.generated.append(response)
            #--- print(callback)

            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    message(st.session_state['generated'][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')

    with st.sidebar:
        uiSidebarInfo()
        uiSidebarWorkingInfo()


if __name__ == '__main__':
    main()