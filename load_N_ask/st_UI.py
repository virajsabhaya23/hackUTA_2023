import streamlit as st

def uiHeroSection():
    st.set_page_config(page_title="Load & Ask", page_icon="robot_face")
    st.write(
        """<style>
        [data-testid="column"] {
            width: calc(50% - 1rem);
            flex: 1 1 calc(50% - 1rem);
            min-width: calc(50% - 1rem);
        }
        </style>""",
        unsafe_allow_html=True,
    )
    st.title('pdf-GPT: Load & Ask 💬 ')
    st.markdown("---")

def uiSidebarInfo():
    """
        Displays information in sidebar
    """
    st.markdown("> version 1.0.2")
    # about this app and instructions CONTAINER
    with st.container():
        st.write("## ℹ️ About this app and instructions")
        with st.expander("Details ...", expanded=True):
            st.markdown(
                "This app uses [OpenAI](https://beta.openai.com/docs/models/overview)'s API to answer questions about your PDF file. \nYou can find the source code on [GitHub](https://github.com/virajsabhaya23/load_N_ask)."
            )
            st.markdown("1. Enter OpenAI API key.\n 2. Upload your PDF file. \n 3. Ask your question.")
    st.write("> made by [Viraj Sabhaya](https://www.linkedin.com/in/vsabhaya23/)")

def uiSidebarWorkingInfo():
    with st.container():
        st.write("## ℹ️ FAQ")
        with st.expander("How does pdf-GPT: Load and Ask work?", expanded=False):
            # st.write("## How does pdf-GPT: Load and Ask work?")
            st.write(":orange[When you upload a document, it will be divided into smaller chunks and stored in a vector index. A vector index is a special type of database that allows for semantic search and retrieval. Semantic search is a type of search that takes into account the meaning of the words in a query, rather than just the words themselves. This allows pdf-GPT to find the most relevant document chunks for a given question.]")
            st.write(":orange[When you ask a question, pdf-GPT will search through the document chunks and find the most relevant ones using the vector index. Then, it will use GPT3 to generate a final answer. GPT3 is a large language model that can generate text, translate languages, write different kinds of creative content, and answer your questions in an informative way.]")

def uiGetOpenAIKey():
    """
        Gets OpenAI API key from user
    """
    st.write('### 1. Enter your OpenAI API key')
    OPENAI_API_KEY = st.text_input(
        help="You can get your API key from https://platform.openai.com/account/api-keys",
        label="WARNING: API key is only free for first 3 months! check OpenAI's policy for upgraded guidelines.",
        type='password',
        placeholder="sk-abcdefghi...",
        # label_visibility="collapsed"
    )
    return OPENAI_API_KEY

def uiGetFileType():
    """
        Gets file type from user
    """
    st.write('### 2. a) Select the type of file you are uploading | ⚠️csv file type is work-in-progress')
    file_type = st.selectbox(
        "Select the type of file you are uploading",
        ("PDF", "CSV")
    )

    st.write(f'### 2. b) Upload your {file_type} file')
    """
        Uploads file
    """
    with st.form(key='my_form', clear_on_submit=True):
        uploaded_file = st.file_uploader(label=f'Upload your {file_type} file', type=[file_type], label_visibility="collapsed")
        submitted = st.form_submit_button(label='UPLOAD!')
    return uploaded_file, file_type, submitted
