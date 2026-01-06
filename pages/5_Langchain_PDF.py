import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain_community.callbacks.manager import get_openai_callback
from Home import footer_section


def main():
    hide_st_style = """
                <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    st.title("Ask your PDF")
    st.header("Ask your PDF 💬")

    # upload file
    pdf = st.file_uploader(
        "Upload your PDF file to feed large language model:", type="pdf"
    )

    # extract the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        with st.expander("Click for extracted text"):
            st.write(text)
        # split into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )
        chunks = text_splitter.split_text(text)
        with st.expander("Click for chunks"):
            st.write(chunks)
        # create embeddings
        embeddings = OpenAIEmbeddings(**st.secrets.openai)
        single_vector = embeddings.embed_query("Konstitucija")
        with st.expander("Click for embeddings"):
            st.write(single_vector[:220])
        # Facebook AI Similarity Search (FAISS)
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        with st.expander("Click for knowledge_base"):
            st.write(knowledge_base)

        # show user input
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = OpenAI(**st.secrets.openai)

            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in docs])

            # Create prompt
            prompt = f"""Answer the question based on the context below:

Context: {context}

Question: {user_question}

Answer:"""

            with get_openai_callback() as cb:
                response = llm.invoke(prompt)
            st.write(response)
            with st.expander("Click for service details"):
                st.write(cb)


if __name__ == "__main__":
    main()
    footer_section()
