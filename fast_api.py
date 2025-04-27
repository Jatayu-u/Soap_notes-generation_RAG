

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
from datasets import load_dataset
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Initialize FastAPI app
app = FastAPI()

# --- Initialization (done once when the server starts) ---

# 1. Configure your OpenAI API key
OPENAI_API_KEY = "your_openai_key"

# 2. Load the SOAP notes dataset
dataset = load_dataset("adesouza1/soap_notes")
train_ds = dataset["train"]
test_ds = dataset["test"]

# 3. Prepare texts and metadata
texts, metadatas = [], []
for split_name, ds in dataset.items():
    for idx, example in enumerate(ds):
        convo_text = example.get("patient_convo", "")
        soap_text = example.get("soap_notes", "")
        metadata = {
            "split": split_name,
            "index": idx,
            "patient_name": example.get("patient_name", "Unknown"),
            "health_problem": example.get("health_problem", ""),
            "soap_notes": soap_text
        }
        texts.append(convo_text)
        metadatas.append(metadata)

# 4. Build FAISS vector store
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

# 5. Create the LLM
llm = OpenAI(temperature=0.2, openai_api_key=OPENAI_API_KEY)

# 6. Create a PromptTemplate for generating SOAP notes
stuff_prompt = PromptTemplate(
    input_variables=["context", "input"],
    template="""You are a helpful medical AI.

Given context from similar past SOAP notes and a new doctor-patient conversation (question),
write a detailed, structured new SOAP note.

Context (previous SOAP notes):
{context}

New Conversation:
{input}

Generate a new SOAP Note (Subjective, Objective, Assessment, Plan):
"""
)

# 7. Create a "stuff" documents chain
document_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=stuff_prompt
)

# 8. Create the Retrieval + Generation Chain
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
rag_chain = create_retrieval_chain(
    retriever=retriever,
    combine_docs_chain=document_chain
)

# 9. Helper function to generate SOAP note
def generate_soap_note(conversation: str) -> str:
    result = rag_chain.invoke({"input": conversation})
    return result["answer"]

# --- API Schema ---

class ConversationRequest(BaseModel):
    conversation: str

class SoapNoteResponse(BaseModel):
    soap_note: str

# --- API Endpoints ---

@app.post("/generate_soap_note", response_model=SoapNoteResponse)
def generate_soap_note_endpoint(request: ConversationRequest):
    try:
        soap_note = generate_soap_note(request.conversation)
        return SoapNoteResponse(soap_note=soap_note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Health Check ---

@app.get("/")
def read_root():
    return {"message": "SOAP Note Generator API is running"}
