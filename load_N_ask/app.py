import os
import sys
import streamlit as st
import pinecone
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import create_csv_agent
from streamlit_chat import message
# lama-2 imports
import replicate
# custom imports
from uiLayouts import uiSidebarInfo, uiSidebarWorkingInfo, uiHeroSection
from readFiles import read_pdf, read_csv
from utils import init_session_state, clear_submit
from splitText import split_text


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


def main():
    # hero section UI component
    uiHeroSection()

    # TODO: Get the API key for LAMA-2 here (replicate)
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
        if replicate_api.startswith('r8_') and len(replicate_api) == 40:
            st.success('API key already provided!', icon='✅')
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    # initialize Pinecone
    pinecone.init(api_key=replicate_api)

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
    else:
        uploaded_file = None

    # Read PDF file and extract text
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.pdf'):
            text = read_pdf(uploaded_file)
            # st.write(text)

        if uploaded_file.name.endswith('.pdf'):
            try:
                with st.spinner("Splitting text into chunks ..."):
                    chunks = split_text(text)
            except Exception as e:
                st.error(e)
            chunks = split_text(text)
            st.write(chunks)
            
        embeddings = HuggingFaceEmbeddings()
        
        # Set up the Pinecone vector database
        index_name = "loadnask"
        index = pinecone.Index(index_name)
        
        documents = [{"id": str(i), "text": chunk} for i, chunk in enumerate(chunks)]
        vectordb = Pinecone.from_documents(documents, embeddings, index_name=index_name)

        llm = replicate(
            model = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
            input = {"temperature": 0.75}
        )

        # Set up the Conversational Retrieval Chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm,
            vectordb.as_retriever(search_kwargs={'k': 2}),
            return_source_documents=True
        )

        # Start chatting with the chatbot
        chat_history = []
        while True:
            query = input('Prompt: ')
            if query.lower() in ["exit", "quit", "q"]:
                print('Exiting')
                sys.exit()
            result = qa_chain({'question': query, 'chat_history': chat_history})
            print('Answer: ' + result['answer'] + '\n')
            chat_history.append((query, result['answer']))
            
        
            
    #     # function to initialize session state
    #     init_session_state()

    #     # Ask question
    #     st.write('### 3. Ask your question'+(f' about {uploaded_file.name}' if uploaded_file else 'uploaded file'))
    #     user_question = st.text_area(on_change=clear_submit, height=90, label="Ask a question about your PDF here :", placeholder="Type your question here", label_visibility="collapsed")

    #     button = st.button("Submit!")
    #     if button or st.session_state.get("submit"):
    #         if not uploaded_file:
    #             st.error("Please upload a file!")
    #         if not user_question:
    #             st.error("Please ask a question!")
    #         else:
    #             st.session_state["submit"] = True
    #             try:
    #                 with st.spinner("Searching for answer..."):
    #                     if file_type.lower().endswith('pdf'):
    #                         response = ask_question(user_question, chunks, OPENAI_API_KEY)
    #                     elif file_type.lower().endswith('csv'):
    #                         response = agent.run(user_question)
    #             except Exception as e:
    #                 st.error(e)
    #         #--- with get_openai_callback() as callback:
    #             # storing past questions and answers
    #             st.session_state.past.append(user_question)
    #             st.session_state.generated.append(response)
    #         #--- print(callback)

    #         if st.session_state['generated']:
    #             for i in range(len(st.session_state['generated'])-1, -1, -1):
    #                 message(st.session_state['generated'][i], key=str(i))
    #                 message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')

    with st.sidebar:
        uiSidebarInfo()
        uiSidebarWorkingInfo()


if __name__ == '__main__':
    main()