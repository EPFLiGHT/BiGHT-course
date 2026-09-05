# Project 8: Conversational AI For Frontline Health Workers

Proposed team size: 5 students.

Project lead: David.

Partner: WHO.

Partner logo: https://upload.wikimedia.org/wikipedia/commons/c/c2/WHO_logo.svg

Keywords: natural language processing, RAG, conversational AI.

## Short Description

Build a chatbot that draws from clinical and national health guidelines in answering questions posed by frontline healthcare workers.

## Motivation

Frontline health workers often need rapid access to trustworthy clinical guidance while working under time pressure, limited supervision, and variable connectivity. National clinical guidelines and approved health guidance may be available, but they can be difficult to search, interpret, or apply during routine care.

This project will focus on building a conversational chatbot interface through which frontline health workers can ask questions and receive responses grounded in the relevant national clinical guidelines and other approved health guidance applicable within the country. The languages of interaction will be English, Khmer, Lao, and Vietnamese.

The main technical focus of the project is on building a reliable RAG system using mmore over country-specific clinical guidance: https://github.com/EPFLiGHT/mmore

Students will identify and collect relevant national clinical guidelines and approved health guidance, and transform these documents into a structured and searchable corpus suitable for multilingual retrieval, including document parsing, cleaning, chunking, and metadata extraction. Students will investigate and compare approaches for multilingual retrieval, reranking, and grounded response generation, with particular attention to ensuring that answers are supported by the appropriate source documents.

The resulting system should be systematically evaluated for retrieval quality, correctness and grounding of generated answers, hallucination or unsupported claims, and performance across the supported languages.

## Intended Users

Potential users include:

- frontline health workers in primary care or community health settings;
- nurses, midwives, and clinical officers seeking quick guidance;
- supervisors supporting health workers across multiple facilities;
- health programs that maintain national clinical guidelines;
- implementation teams evaluating multilingual digital health tools.

## Possible Features

Possible features include:

- ingestion and indexing of national clinical guidelines and approved health guidance;
- retrieval-augmented generation over guideline documents;
- multilingual question answering in English, Khmer, Lao, and Vietnamese;
- source citations or excerpts for each answer;
- answer confidence, uncertainty, or escalation guidance;
- conversation history for follow-up questions;
- guardrails for out-of-scope, unsafe, or emergency questions;
- lightweight interface for mobile or low-resource settings;
- evaluation dashboard for answer quality and retrieval performance.

The team should avoid building a general medical chatbot. The system should be explicitly grounded in approved guidance and should make clear when a question cannot be answered from the available documents.

## Design Questions

Consider:

- Which guideline documents are in scope, and how should they be chunked or indexed?
- How should the system handle questions that require local policy, clinical judgment, or urgent escalation?
- How can answers remain faithful to the retrieved guidance instead of relying on model memory?
- What does a useful citation or evidence excerpt look like for a busy frontline health worker?
- How should multilingual interaction work across English, Khmer, Lao, and Vietnamese?
- What should happen when retrieval fails or retrieved passages disagree?
- How can the interface communicate limitations without making the tool unusable?

## Technical Directions

Possible technical components include:

- document ingestion pipeline for clinical and national health guidelines;
- text cleaning, chunking, metadata extraction, and provenance tracking;
- retrieval system using embeddings or keyword search;
- RAG pipeline with source-grounded answer generation;
- multilingual translation, cross-lingual retrieval, or multilingual embeddings;
- prompt design and clinical-safety guardrails;
- answer citation and source display;
- evaluation dataset of representative frontline-worker questions;
- automated and manual evaluation of retrieval quality, faithfulness, and answer usefulness.

The prototype should be reproducible from the project repository and should not depend on undocumented document collections, hidden prompts, or unavailable APIs unless those constraints are explicitly documented.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid source-grounded question-answering path for frontline health workers.

Minimum convincing POC:

- the team ingests a documented set of approved clinical or national health guidance;
- the system retrieves relevant passages for representative health-worker questions;
- the chatbot generates answers grounded in retrieved sources;
- answers include citations, source snippets, or clear references back to the guidance;
- the interface supports at least one multilingual interaction path relevant to English, Khmer, Lao, or Vietnamese;
- the system handles at least one out-of-scope or unsafe question by refusing, escalating, or asking for clarification;
- the team reports retrieval and answer-quality results on a small evaluation set.

The POC may use a limited guideline corpus, a small set of diseases or workflows, and a simple chat interface. It should not be only a generic chatbot prompt without retrieval, citations, and evaluation.

## Evaluation Ideas

Possible evaluation approaches include:

- measuring retrieval precision or recall on a set of guideline-grounded questions;
- checking whether answers are faithful to cited passages;
- comparing RAG answers with answers generated without retrieval;
- evaluating multilingual questions for semantic preservation and answer usefulness;
- testing refusal or escalation behavior for unsafe, emergency, or out-of-scope questions;
- collecting expert or staff review of answer clarity, safety, and usefulness;
- analyzing common failure modes such as missing guidance, wrong citations, hallucinated recommendations, or overconfident answers.

## Final Demo Target

The final demo should show a frontline health worker asking clinical or guideline questions through a chat interface. The system should retrieve relevant guidance, answer in a supported language, show the source evidence behind the answer, and demonstrate how it handles uncertainty, missing information, or unsafe requests.
