# AI Research Assistant Backend

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from Dataprocessing import process_file, retrieve_chunks

load_dotenv()


# ------------------------------------------------------------- MODEL -------------------------------------------------------------

# Initialize Mistral model
model = init_chat_model(
    "mistral-small-latest",
    model_provider="mistralai"
)


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


# ------------------------------------------------------------- DOCUMENT PROCESSING + RETRIEVAL -------------------------------------------------------------

def answer_question(question, file_paths):

    try:

        all_processed_chunks = []

        for file_path in file_paths:

            processed_chunks = process_file(file_path)

            all_processed_chunks.extend(processed_chunks)

        if not all_processed_chunks:

            return (
                "I could not extract any text from the uploaded document. "
                "Please upload a text-based PDF, DOCX, TXT, or PPTX file."
            )

        retrieved_chunks = retrieve_chunks(
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

    except Exception as e:

        return (
            "Sorry, I was unable to process the research files. "
            "Please check the uploaded files and try again."
        )