from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()

model=init_chat_model("mistral-small-latest",model_provider="mistralai")
def build_prompt(question, retrieved_chunks):
    context=""
    for chunk in retrieved_chunks:
        context=context+chunk["text"]+"\n"
        context=context+"Source: "+chunk["source"]+"\n"
        context=context+"Page Number: "+str(chunk.get("page", "N/A"))+"\n"

    prompt = """
    You are an AI research assistant.
    Use the provided research context to answer for queries asked by user.
    If answer is not available in the context,say there is not enough information to answer your query.
    Research Context: """
    prompt=prompt+context
    prompt=prompt+"\nUser Question: "+question
    return prompt

def get_answer(question,retrieved_chunks):
    prompt = build_prompt(question, retrieved_chunks)
    response=model.invoke(prompt)
    return response.content

test_chunks = [
    {
        "text": "The CNN model achieved an accuracy of 94%.",
        "source": "paper1.pdf",
        "page": 8
    }
]

test_question = "What accuracy did the CNN model achieve?"

test_answer = get_answer(test_question, test_chunks)

print(test_answer)