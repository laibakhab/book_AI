# Tasks: RAG Knowledge Ingestion Pipeline

**Feature**: RAG Knowledge Ingestion Pipeline
**Branch**: `002-rag-ingestion-pipeline`
**Created**: 2025-12-16
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)
**Input**: Create backend folder and initialize project with UV package manager for "cohere" and "qdrant" clients, fetch clean, and chunk text from deployed URLs, generate embeddings and upsert into Qdrant with metadata only in one file named main.py

## Dependencies

- User Story 1 (Build Searchable Knowledge Base) - Priority: P1 (Base requirement for other stories)
- User Story 2 (Configure Ingestion Parameters) - Priority: P2 (Depends on basic pipeline from US1)
- User Story 3 (Monitor Ingestion Process) - Priority: P3 (Depends on basic pipeline from US1)

## Parallel Execution Examples

- T002-T005: Project structure setup tasks can run in parallel
- T008-T010: Different components of the core pipeline can be developed in parallel
- T015-T018: Chunking, embedding, and storage functions can be developed in parallel

## Implementation Strategy

This implementation will follow an incremental delivery approach:
1. MVP: Basic crawler that saves content to Qdrant (US1 only)
2. Enhanced: Add configuration options (US2)
3. Complete: Add monitoring capabilities (US3)

---

## Phase 1: Setup

Goal: Initialize project with proper structure, dependencies, and environment

- [x] T001 Create backend directory structure in project root
- [x] T002 Initialize project with UV package manager in backend directory
- [x] T003 Add cohere and qdrant-client dependencies to pyproject.toml
- [x] T004 Create main.py file in backend directory
- [x] T005 Set up .env file for API keys and configuration

## Phase 2: Foundational Components

Goal: Build core components required by all user stories

- [x] T006 [P] Install and configure Cohere client in main.py
- [x] T007 [P] Install and configure Qdrant client in main.py
- [x] T008 [P] Define function to get all URLs from deployed site (https://physical-ai-hackathon-red.vercel.app/)
- [x] T009 [P] Define function to extract text from URL in main.py
- [x] T010 [P] Define function to chunk text in main.py
- [x] T011 [P] Define function to create embeddings in main.py
- [x] T012 [P] Define function to create Qdrant collection named 'rag_embeddings'
- [x] T013 [P] Define function to save chunk to Qdrant with metadata in main.py
- [x] T014 Implement error handling and logging in main.py

## Phase 3: User Story 1 - Build Searchable Knowledge Base [US1]

Goal: As a developer implementing a RAG chatbot, I want to automatically ingest content from a Docusaurus-based book website, so that I can create a searchable vector knowledge base that enables accurate responses to user queries.

Independent Test: The system can discover and crawl a Docusaurus book site and store its content in a vector database, allowing basic search functionality to be demonstrated.

- [x] T015 [US1] Implement get_all_urls function to crawl https://physical-ai-hackathon-red.vercel.app/
- [x] T016 [US1] Implement extract_text_from_url function to clean text from crawled pages
- [x] T017 [US1] Implement chunk_text function with configurable size limits
- [x] T018 [US1] Implement embed function using Cohere models
- [x] T019 [US1] Implement create_collection function to create 'rag_embeddings' collection
- [x] T020 [US1] Implement save_chunk_to_qdrant function with metadata
- [x] T021 [US1] Create main execution function that orchestrates the entire pipeline
- [ ] T022 [US1] Test pipeline with sample URLs from the deployed site
- [ ] T023 [US1] Verify data is properly stored in Qdrant with accessible metadata

## Phase 4: User Story 2 - Configure Ingestion Parameters [US2]

Goal: As an AI engineer, I want to configure ingestion parameters like chunk size, embedding model, and metadata extraction rules, so that I can optimize the knowledge base for my specific use case.

Independent Test: Different configurations produce appropriately-sized chunks with different metadata in the vector database.

- [x] T024 [US2] Add configuration options to .env file for chunk size limits (512-4096 tokens)
- [x] T025 [US2] Add configuration option for Cohere model selection
- [x] T026 [US2] Add configuration options for metadata extraction rules
- [x] T027 [US2] Modify chunk_text function to use configurable chunk size
- [x] T028 [US2] Modify embed function to use configurable Cohere model
- [x] T29 [US2] Add configurable metadata fields to save_chunk_to_qdrant function
- [ ] T030 [US2] Test pipeline with different configuration settings

## Phase 5: User Story 3 - Monitor Ingestion Process [US3]

Goal: As an operator, I want to monitor the ingestion pipeline progress and health, so that I can detect and troubleshoot issues during the process.

Independent Test: The system logs ingestion progress and errors that are accessible to operators.

- [x] T031 [US3] Add progress tracking to the main pipeline execution
- [x] T032 [US3] Implement comprehensive error logging for failed documents/processing steps
- [x] T033 [US3] Add metrics collection for processed pages, errors, and processing time
- [ ] T034 [US3] Create monitoring dashboard endpoint/functionality
- [ ] T035 [US3] Add notification mechanism for pipeline failures
- [ ] T036 [US3] Test monitoring functionality with various error scenarios

## Phase 6: Polish & Cross-Cutting Concerns

Goal: Complete the implementation with additional functionality and quality improvements

- [ ] T037 Implement rate limiting for web crawling to avoid overwhelming source servers
- [ ] T038 Add handling for non-English content or multilingual books
- [ ] T039 Add handling for authentication (skip pages requiring authentication with warning)
- [ ] T040 Add data retention policy (store data indefinitely until manually deleted)
- [ ] T041 Add tests for all major functions
- [ ] T042 Document the API and usage instructions in README.md
- [ ] T043 Optimize performance based on success criteria (process 1000 pages within 2 hours)
- [ ] T044 Run end-to-end tests to verify all requirements are met