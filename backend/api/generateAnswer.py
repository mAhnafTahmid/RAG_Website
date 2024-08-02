import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_pinecone import PineconeVectorStore
import pinecone
from langchain.chains import RetrievalQA
from langchain_huggingface.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.llms import HuggingFaceHub

# from langchain import HuggingFaceHub


def setup_vectorstore_and_search(query, k=3):
    # Load the environment variables from .env file
    load_dotenv()

    HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # Use environment variable for authentication
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

    # Initialize Pinecone
    pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    # Connect to the existing Pinecone index
    index_name = "langchain-retrieval-augmentation"
    index = pc.Index(index_name)

    hf_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Initialize Pinecone vectorstore
    vectorstore = PineconeVectorStore(
        index=index,
        text_key="text",
        embedding=hf_embeddings,  # Ensure this matches your data schema
    )

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={"temperature": 0, "max_length": 64},
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    answer = qa.invoke(query)

    return answer


# if __name__ == "__main__":
#     query = "who was Benito Mussolini?"
#     result = setup_vectorstore_and_search(query)
#     print(result)
