# The Fourcasters

## AI Research Assistant

An AI-powered research assistant that helps users analyze and understand multiple research documents using document processing, retrieval-augmented generation (RAG), and a large language model.

## Problem Statement

Researchers often need to read and compare information across multiple papers, which can be time-consuming and difficult when the information is spread across different documents.

Finding relevant information, comparing research findings, and identifying differences between papers manually can take significant time.

## Our Solution

The Fourcasters is an AI-powered research assistant that allows users to upload research documents and interact with their content using natural-language questions.

The system processes the uploaded documents, retrieves relevant information, and uses an LLM to generate answers grounded in the provided research context.

When multiple research documents are uploaded, the system can compare relevant information and present the comparison in a structured table while providing source and page references where available.

#How Our Project Is Different:
Multi-document analysis — users can upload and search multiple documents together.
Semantic search — uses Mistral embeddings and cosine similarity instead of relying only on keyword matching.
Context-grounded answers — the LLM answers using information retrieved from the uploaded documents.
Source tracking — preserves page, paragraph, and slide information to help verify answers.
Document summarization — generates concise summaries of uploaded documents.
Multi-document comparison — combines relevant information from different documents and presents comparisons.
Multiple file formats — supports PDF, DOCX, TXT, and PPTX.
Natural-language interaction — users can ask questions normally instead of manually searching documents.
Reduced hallucination risk — prompts instruct the model not to invent information outside the retrieved context.
Simple Streamlit interface — provides document upload, processing, summaries, chat, and source viewing in one place.
 Real-World Applications 
 • Academic research: search and compare research papers and generate summaries. 
 • Corporate knowledge bases: answer questions from internal reports, policies, manuals, and documentation. 
 • Education: allow students to question textbooks, notes, and study material. 
 • Technical documentation: help engineers locate procedures and specifications. 
 • Research and development: compare methods, datasets, findings, and conclusions. 
 • Legal document review: locate relevant clauses across large document sets, subject to professional validation.
