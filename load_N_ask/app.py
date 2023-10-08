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

# custom imports
from uiLayouts import uiSidebarInfo, uiSidebarWorkingInfo, uiHeroSection #image_custom
from readFiles import read_pdf, read_csv, read_txt
from utils import init_session_state, clear_submit
from splitText import split_text


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
    # st.write(docs)
    llms = OpenAI(openai_api_key=OPENAI_API_KEY)
    qa_chain = load_qa_chain(llms, chain_type="stuff")
    response = qa_chain.run(input_documents=docs, question=user_question)
    # st.write(response)
    return response


def main():
    uiHeroSection()
    # image_custom()
    # get API key from USER
    st.write('### 1. Enter your OpenAI API key')
    OPENAI_API_KEY = st.text_input(
        help="You can get your API key from https://platform.openai.com/account/api-keys",
        label="WARNING: API key is only free for first 3 months! check OpenAI's policy for upgraded guidelines.",
        type='password',
        placeholder="sk-abcdefghi...",
        # label_visibility="collapsed"
    )
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    # get the option from user what file they are importing
    st.write('### 2. a) Select the type of file you are uploading | ⚠️csv file type is work-in-progress')
    file_type = st.selectbox(
        "Select the type of file you are uploading",
        ("PDF", "CSV")
    )

    # Upload PDF file
    st.write(f'### 2. b) Upload your {file_type} file')
    if file_type.lower().endswith('pdf'):
        uploaded_file = st.file_uploader('Upload your PDF file', type=['pdf'], label_visibility="collapsed")
        st.write(uploaded_file)
    elif file_type.lower().endswith('csv'):
        uploaded_file = st.file_uploader('Upload your CSV file', type=['csv'], label_visibility="collapsed")
        st.write(uploaded_file)
    elif file_type.lower().endswith('txt'):
        uploaded_file = st.file_uploader('Upload your TXT file', type=['txt'], label_visibility="collapsed")
        st.write(uploaded_file)
    else:
        uploaded_file = None

    # Read PDF file and extract text
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.pdf'):
            text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.csv'):
            st.write(text)
            agent = create_csv_agent(OpenAI(openai_api_key=OPENAI_API_KEY,temperature=0), uploaded_file.name, verbose=True)
            st.write(agent)
        # TODO: add support for other file types
        #     text=read_pdf(uploaded_file)
        # elif uploaded_file.name.endswith('.txt'):
        #     text=parse_text(uploaded_file)
        # elif uploaded_file.name.endswith('.docx'):
        #     text=parse_docx(uploaded_file)
        else:
            raise ValueError("File type not supported")

        if uploaded_file.name.endswith('.pdf'):
            try:
                with st.spinner("Splitting text into chunks ..."):
                    chunks = split_text(text)
            except OpenAIError as e:
                st.error(e._message)
            chunks = split_text(text)
            # st.write(chunks)

    # read CSV file and extract text
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            try:
                with st.spinner("Splitting text into chunks ..."):
                    chunks = read_csv(uploaded_file)
            except OpenAIError as e:
                st.error(e._message)
            chunks = read_csv(uploaded_file)
            # st.write(chunks)

    # read TXT file and extract text
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.txt'):
            try:
                with st.spinner("Splitting text into chunks ..."):
                    chunks = read_txt(uploaded_file)
            except OpenAIError as e:
                st.error(e._message)
            chunks = read_txt(uploaded_file)
            # st.write(chunks)



        # function to initialize session state
        init_session_state()

        # Ask question
        st.write('### 3. Ask your question'+(f' about {uploaded_file.name}' if uploaded_file else 'uploaded file'))
        user_question = st.text_area(on_change=clear_submit, height=90, label="Ask a question about your PDF here :", placeholder="Type your question here", label_visibility="collapsed")

        button = st.button("Submit!")
        if button or st.session_state.get("submit"):
            if not uploaded_file:
                st.error("Please upload a file!")
            if not user_question:
                st.error("Please ask a question!")
            else:
                st.session_state["submit"] = True
                try:
                    with st.spinner("Searching for answer..."):
                        if file_type.lower().endswith('pdf'):
                            response = ask_question(user_question, chunks, OPENAI_API_KEY)
                        elif file_type.lower().endswith('csv'):
                            response = agent.run(user_question)
                        elif file_type.lower().endswith('txt'):
                            response = ask_question(user_question, chunks, OPENAI_API_KEY)
                        else:
                            raise ValueError("File type not supported")
                except Exception as e:
                    st.error(e)
            #--- with get_openai_callback() as callback:
                # storing past questions and answers
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