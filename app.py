
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from transformers import pipeline
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from HTMLLoader import html_splitter
from langchain_together import Together
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

app = Flask(__name__)
CORS(app)
load_dotenv()

# Initialize global variables to store preloaded content and vector store
preloaded_content = None
vectorstore = None
model_name = "BAAI/bge-base-en-v1.5"
encode_kwargs = {"normalize_embeddings": False}
embedding_function = HuggingFaceBgeEmbeddings(model_name=model_name, encode_kwargs=encode_kwargs)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Define a simple and versatile prompt template
prompt = PromptTemplate(
    input_variables=['context', 'question'],
    template='''
    Your name is Kanha. You are an assistant for question answering tasks.Use the following pieces of retrieved context and your own knowledge to answer the question. If the question is not related to the context then treat it as general conversation and just give a general answer.
    Do not add any examples or extra information related to given context in case of general conversation i.e. when user query is unrelated to context. In general conversation just tell
    "hello, I am Kanha, your chat assistant, ask any queries only related to the webpage opened.
    Keep answers brief, concise but to the point and keep the answer only related to the query,do not add any information that is not asked .
    
    -->Operational Guidelines:

    Ensure responses are succinct and directly relevant to the inquiry.
    Do not include personal opinions or unnecessary examples.
    Aim to enhance the user's experience by providing clear and accurate information.
    
    Context: {context}
    Query: {question}
    Answer:

    '''
 )
# def prepare_prompt(context, question):
#     if context == "General conversation":
#         introduction = "Your name is Kanha. You are an assistant for question answering tasks. You are designed to make user's information searching easier. You can answer only queries related to this page only.Just give your inroduction as answer using the previous lines"
#     else:
#         introduction = "Your name is Kanha. You are an assistant for question answering tasks.Use the following pieces of retrieved context and your own knowledge to answer the question. If you don't know the answer, just tell your name and brief introduction and say you don't know the answer. Keep answers descriptive with bullet points and mention the process."

#     # Construct the complete prompt
#     prompt_text = f"{introduction}\nQuestion: {question}\nContext: {context}\nAnswer:"
#     return prompt_text

@app.route('/')
def index():
    return "Your chat guide Kanha is here"

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/preload', methods=['POST'])
def preload_content():
    global preloaded_content, vectorstore
    data = request.json
    url = data['url']

    # Dynamically update the URLs list
    urls = [url]

    # Split and store the page content
    splits = html_splitter(urls)
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_function, persist_directory="../chroma_db")
    
    preloaded_content = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    return jsonify({"message": "Content preloaded successfully"})

@app.route('/query', methods=['POST'])
def handle_query():
    global preloaded_content, vectorstore
    data = request.json
    query = data['query']
    print("Received query:", type(query))
    if preloaded_content is None:
        return jsonify({"error": "Content not preloaded"}), 400

    # Extract the query embedding
    #query_embedding = embedding_function.embed_query(query[0])

    # Perform similarity search to determine context
    similar_docs = vectorstore.search(query,search_type="similarity" ,k=1)  # Assuming k=1 for simplicity
    if similar_docs:
        context = format_docs(similar_docs)
    else:
        context = "General conversation"  # Fallback if no similar documents are found

    # Using Together API for generating responses
    response = Together(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        together_api_key=os.getenv("TOGETHER_API_KEY"),
        temperature=0.3,
        max_tokens=512
    )

    # rag_chain = (
    #     {"context": context, "question": RunnablePassthrough()}
    #     | prompt
    #     | response
    # )
    input_prompt=prompt.format(context=context,question=query)#prepare_prompt(context,query)
    answer = response(input_prompt)
    #print(answer)
    
    return jsonify({"answer": answer})

@app.route('/clear_chromadb', methods=['POST'])
def clear_chromadb():
    global vectorstore
    vectorstore = None  # or add logic to destroy the database
    return jsonify({"message": "ChromaDB cleared successfully"})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
