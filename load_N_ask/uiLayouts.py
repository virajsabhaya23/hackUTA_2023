import streamlit as st
import streamlit as st
from PIL import Image
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

def uiHeroSection():
    st.set_page_config(page_title="Load & Ask", page_icon="robot_face")
    st.write(
        """<style>
        [data-testid="column"] {
            width: calc(50% - 1rem);
            flex: 1 1 calc(50% - 1rem);
            min-width: calc(50% - 1rem);
            display: flex;
            align-items: flex-end;
        }
        </style>""",
        unsafe_allow_html=True,
    )
    text_column, image_column = st.columns((2, 1)) 
    with text_column:
        st.title(' Load & Ask 💬 ')
    with image_column:
        lottie_coding = load_lottieurl("https://lottie.host/f9999102-82ea-48f3-a43e-555e1b508ad2/Fh853fMk3Z.json")
        st_lottie(lottie_coding, speed=1, height=200, key="coding")
    st.markdown("---")



# def image_custom():
#     lottie_coding=load_lottieurl("https://lottie.host/f9999102-82ea-48f3-a43e-555e1b508ad2/Fh853fMk3Z.json")
#     st_lottie(lottie_coding, speed=1, height=300, key="coding")

def uiSidebarInfo():
    """
        Displays information in sidebar
    """
    st.markdown("> version 1.0.0")
    # about this app and instructions CONTAINER
    # with st.container():
    #     st.write("## ℹ️ About this app and instructions")
    #     with st.expander("Details ...", expanded=True):
    #         st.markdown(
    #             "This app uses [OpenAI](https://beta.openai.com/docs/models/overview)'s API to answer questions about your PDF file. \nYou can find the source code on [GitHub](https://github.com/virajsabhaya23/load_N_ask)."
    #         )
    #         st.markdown("1. Enter OpenAI API key.\n 2. Upload your PDF file. \n 3. Ask your question.")
    st.write("> made by [Viraj Sabhaya](https://www.linkedin.com/in/vsabhaya23/), [Jaime Barajas](https://www.linkedin.com/in/jaime-barajas-1a7b42191/), [Kevin Ventura](https://www.linkedin.com/in/kevin-ventura-3207041ba/), [Zaineel Mithani](https://www.linkedin.com/in/zaineel-mithani-19588025b/)")

def uiSidebarWorkingInfo():
    with st.container():
        st.write("## ℹ️ FAQ")
        with st.expander("How does Load and Ask work?", expanded=False):
            # st.write("## How does Load and Ask work?")
            st.write(":orange[When you upload a document, it will be divided into smaller chunks and stored in a vector index. A vector index is a special type of database that allows for semantic search and retrieval. Semantic search is a type of search that takes into account the meaning of the words in a query, rather than just the words themselves. This allows to find the most relevant document chunks for a given question.]")
            st.write(":orange[When you ask a question, will search through the document chunks and find the most relevant ones using the vector index. Then, it will use GPT3 to generate a final answer. GPT3 is a large language model that can generate text, translate languages, write different kinds of creative content, and answer your questions in an informative way.]")
