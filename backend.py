from dotenv import load_dotenv
load_dotenv()

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
test_chunks = [
    {
        "text": "The CNN model achieved an accuracy of 94%.",
        "source": "paper1.pdf",
        "page": 8
    }
]

test_question = "Which model performed best?"

test_prompt = build_prompt(test_question, test_chunks)

print(test_prompt)