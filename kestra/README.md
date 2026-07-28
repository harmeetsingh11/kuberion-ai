# Kestra Workflow

This workflow orchestrates the document ingestion pipeline.

It executes:

1. Extract documents
2. Clean documents
3. Parse documents
4. Chunk documents
5. Generate embeddings
6. Build retrieval indexes

The workflow is optional because pre-generated embeddings and indexes are already included in the repository for faster startup.