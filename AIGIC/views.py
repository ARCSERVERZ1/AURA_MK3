import time
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

aigic_config = {
    "embedding": "models/embedding-001",
    "apikey": "AIzaSyARuT8pYU-yNcGWV40Z-3BYcQgvzIuzs7A",
    "model": "gemini-2.0-flash",
    "temperature": 0.3,
    "vector_db_name": "11DB"
}

embedding_model = GoogleGenerativeAIEmbeddings(model=aigic_config['embedding'], google_api_key=aigic_config['apikey'])
llm = ChatGoogleGenerativeAI(model=aigic_config['model'], temperature=aigic_config['temperature'],
                             google_api_key=aigic_config['apikey'])



@api_view(['POST'])
def load_vector_db(requests):
    docs = ['Sanjay and avinash are brothers and their parents are RANI and Veera Babu and live in kakinada']
    new_db = FAISS.from_texts(docs, embedding=embedding_model)
    new_db.save_local(aigic_config["vector_db_name"])
    print(" [+] Vector DB Updated")
    return JsonResponse({'status': 'DB Updated'}, safe=True)


def build_chain():
    prompt_template = """
    Use the following context to answer the question as accurately as possible.
    If the answer is not in the context, respond with: "Answer not available in the context".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    return LLMChain(llm=llm, prompt=prompt)


@api_view(['POST'])
def rag_query(requests):
    k = 4

    print(requests.data)
    question = requests.data["query"]
    start = time.time()
    vector_db = FAISS.load_local(aigic_config["vector_db_name"], embedding_model, allow_dangerous_deserialization=True)
    docs = vector_db.similarity_search(question, k=k)
    context = "\n\n".join(doc.page_content for doc in docs)
    chain = build_chain()
    response = chain.invoke({"context": context, "question": question})
    print(f"⏱ Response time: {time.time() - start:.2f}s")
    res = {'output_text': response["text"],
           'time_taken': f"{time.time() - start:.2f}s"}
    return JsonResponse( res , safe = False)
