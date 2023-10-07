# [pdf-GPT: Load and Ask](https://virajsabhaya23-load-n-ask-app-syntut.streamlit.app/)

This is a Streamlit app that uses OpenAI's API to answer questions about your PDF file. 

<img width="420" height="100%" alt="Screenshot 2023-05-07 at 15 19 31" src="https://user-images.githubusercontent.com/77448246/236704768-045a8a20-b1c2-47b6-8dd0-ddecf1d48fb7.png">

## TODOs:
- [ ] Implement support for docx, and txt files
- [ ] Able to provide source for the answer provided
- [ ] Implement OpenSource AI API as another option model, apart from GPT 3.5

## Requirements

The following packages are required to run this app:

- streamlit
- streamlit-chat
- PyPDF2
- langchain
- faiss
- openai
- tiktoken
- requests
- docx2txt

To install these packages, you can run:

```
pip install -r requirements.txt
```

## How to use

To use this app, follow these steps:

1. Enter your OpenAI API key.
2. Upload your PDF file.
3. Ask your question about the PDF file.

The app will then search for the answer to your question in the uploaded PDF file using the OpenAI API. The answer will be displayed in the "Past questions and answers" section.

## About the author

This app was created by [Viraj Sabhaya](https://www.linkedin.com/in/vsabhaya23/). You can find the code for this app on [GitHub](https://github.com/virajsabhaya23/load_N_ask).
