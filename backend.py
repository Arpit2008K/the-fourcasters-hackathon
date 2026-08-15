# Test LLM integration using Mistral

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
    Use the provided research context to answer the user's query.
    If answer is not available in the context, say there is not enough information to answer your query.
    Do not invent or assume information that is not present in the research context.
    When answering, mention the relevant source and page number from the research context when available.
    When information from multiple sources is relevant, combine the information and clearly identify the sources.
    If information from different sources conflicts, clearly state that the sources disagree and present the conflicting information without choosing one unless the context provides evidence to support a conclusion.
    If multiple research documents are provided, automatically compare the relevant documents and present the comparison in a clear table, even if the user does not explicitly ask for a comparison.
    Only include information supported by the research context in the comparison table, and do not fill missing information with assumptions.
    Research Context: """
    prompt=prompt+context
    prompt=prompt+"\nUser Question: "+question
    return prompt

def get_answer(question,retrieved_chunks):
    try:
        prompt = build_prompt(question, retrieved_chunks)
        response=model.invoke(prompt)
        return response.content
    except Exception as e:
        return "Sorry, I was unable to give you an answer.Please try again."

test_chunks = [
    {
        "text": "This study used a CNN model and achieved an accuracy of 94%. The model was trained on the ImageNet dataset.",
        "source": "paper1.pdf",
        "page": 5
    },
    {
        "text": "This study used an SVM model and achieved an accuracy of 88%. The model was trained on the CIFAR-10 dataset.",
        "source": "paper2.pdf",
        "page": 7
    }
]
test_question = "What are the differences between the two research papers?"
test_answer = get_answer(test_question, test_chunks)

print(test_answer)