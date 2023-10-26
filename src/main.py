import os
import argparse
from dotenv import load_dotenv
from utils import parse_github_url, get_files_from_github_repo, fetch_md_contents, get_source_chunks
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Fetch all *.md files from a GitHub repository.")
    parser.add_argument("url", help="GitHub repository URL")
    args = parser.parse_args()

    GITHUB_OWNER, GITHUB_REPO = parse_github_url(args.url)
    
    all_files = get_files_from_github_repo(GITHUB_OWNER, GITHUB_REPO, os.getenv("github_access_key"))

    CHROMA_DB_PATH = f'./chroma/{os.path.basename(GITHUB_REPO)}'

    chroma_db = None

    if not os.path.exists(CHROMA_DB_PATH):
        print(f'Creating Chroma DB at {CHROMA_DB_PATH}...')
        source_chunks = get_source_chunks(all_files)
        chroma_db = Chroma.from_documents(source_chunks, OpenAIEmbeddings(openai_api_key=os.getenv("openai_api_key")), persist_directory=CHROMA_DB_PATH)
        chroma_db.persist()
    else:
        print(f'Loading Chroma DB from {CHROMA_DB_PATH} ... ')
        chroma_db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=OpenAIEmbeddings(openai_api_key=os.getenv("openai_api_key")))

    qa_chain = load_qa_chain(OpenAI(model_name="text-davinci-003", temperature=0.7, openai_api_key=os.getenv("openai_api_key")), chain_type="stuff")
    qa = RetrievalQA(combine_documents_chain=qa_chain, retriever=chroma_db.as_retriever())

    while True:
        print('\n\n\033[31m' + 'Ask a question' + '\033[m')
        user_input = input()
        print('\033[31m' + qa.run(user_input) + '\033[m')

if __name__ == "__main__":
    main()