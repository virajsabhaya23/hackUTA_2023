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
