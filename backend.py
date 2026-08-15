# AI Research Assistant Backend
import numpy as np
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from Dataprocessing import process_file, retrieve_chunks
from langchain_mistralai import MistralAIEmbeddings

load_dotenv()


# ------------------------------------------------------------- MODEL -------------------------------------------------------------

# Initialize Mistral model
model = init_chat_model(
    "mistral-small-latest",
    model_provider="mistralai"
)
embedding_model = MistralAIEmbeddings(model = "mistral-embed")

# EMBEDDING FUNCTION
def embed_chunks(chunks):
    """Compute and attach an 'embedding' vector to each chunk dict in place."""
    if not chunks:
        return chunks
    texts = [chunk["text"] for chunk in chunks]
    vectors = embedding_model.embed_documents(texts)
    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector
    return chunks

def embed_query(text):
    return embedding_model.embed_query(text)

def cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
 
 
def semantic_retrieve(question, chunks, top_k=5):
    """Retrieve the top_k most semantically similar chunks to the question."""
    embedded_chunks = [c for c in chunks if c.get("embedding") is not None]
    if not embedded_chunks:
        return []
 
    query_vector = embed_query(question)
 
    scored_chunks = []
    for chunk in embedded_chunks:
        score = cosine_similarity(query_vector, chunk["embedding"])
        scored_chunks.append((score, chunk))
 
    scored_chunks.sort(key=lambda item: item[0], reverse=True)
 
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
# ------------------------------------------------------------- PROMPT -------------------------------------------------------------

def build_prompt(question, retrieved_chunks):

    context = ""

    for chunk in retrieved_chunks:

        context = context + chunk["text"] + "\n"

        context = (context+ "Source: "+ chunk["source"]+ "\n")

        context = (context+ "Page Number: "+ str(chunk.get("page", "N/A"))+ "\n")

    prompt = """
        You are an AI research assistant.
        Use the provided research context to answer the user's query.
        If the answer is not available in the context, say:
        "There is not enough information to answer your query."
        Do not invent or assume information that is not present in the research context.
        When answering, mention the relevant source and page number from the research context when available.
        When information from multiple sources is relevant, combine the information and clearly identify the sources.
        If information from different sources conflicts, clearly state that the sources disagree and present the conflicting information without choosing one unless the context provides evidence to support a conclusion.
        If multiple research documents are provided, automatically compare the relevant documents and present the comparison in a clear table, even if the user does not explicitly ask for a comparison.
        Only include information supported by the research context in the comparison table, and do not fill missing information with assumptions.
        Research Context: """

    prompt = prompt + context

    prompt = prompt + "\nUser Question: " + question

    return prompt


# ------------------------------------------------------------- ANSWER -------------------------------------------------------------

def get_answer(question, retrieved_chunks):

    try:

        prompt = build_prompt(
            question,
            retrieved_chunks
        )

        response = model.invoke(prompt)

        return response.content

    except Exception as e:

        return "Sorry, I was unable to give you an answer. Please try again."

# SUMMARIZATION 
def summarize_document(source_name,chunks,max_words=6000):
    """Generate a concise summary of a single document from its chunks."""
    document_chunks = [c for c in chunks if c["source"] == source_name]
    if not document_chunks:
        return "No content found for this document."
 
    document_chunks.sort(key=lambda c: (c.get("page", 0), c.get("paragraph", 0), c.get("slide", 0), c["chunk"]))
 
    full_text = " ".join(c["text"] for c in document_chunks)
    words = full_text.split()
    if len(words) > max_words:
        full_text = " ".join(words[:max_words])
 
    prompt = f"""
        You are an AI research assistant.
        Summarize the following research document titled "{source_name}" concisely.
        Cover the main objective, key findings or methodology, and conclusions.
        Base the summary only on the content provided below. Do not invent or assume
        information that is not present in the text.
 
        Document Content:
        {full_text}
        """
    try:
        response = model.invoke(prompt)
        return response.content
    except Exception:
        return "Sorry, I was unable to generate a summary. Please try again."
# ------------------------------------------------------------- DOCUMENT PROCESSING + RETRIEVAL -------------------------------------------------------------

def answer_question(question, file_paths):

    try:

        all_processed_chunks = []

        for file_path in file_paths:

            processed_chunks = process_file(file_path)
            embed_chunks(processed_chunks)
            all_processed_chunks.extend(processed_chunks)

        if not all_processed_chunks:

            return (
                "I could not extract any text from the uploaded document. "
                "Please upload a text-based PDF, DOCX, TXT, or PPTX file."
            )

        retrieved_chunks = semantic_retrieve(
            question,
            all_processed_chunks
        )

        if not retrieved_chunks:

            return (
                "I could not find relevant information in the uploaded "
                "documents to answer this question."
            )

        return get_answer(
            question,
            retrieved_chunks
        )

    except Exception:

        return (
            "Sorry, I was unable to process the research files. "
            "Please check the uploaded files and try again."
        )