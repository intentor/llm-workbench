"""Manages indexing of files in a vector database."""

from logging import getLogger
from typing import Sequence

from chromadb.api.models.Collection import Collection
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode
from ollama import Client
import chromadb

logger = getLogger()


class ContextIndexer():
    """Manages indexing files."""

    def __init__(
        self,
        ollama: Client,
        db_path: str,
        collection_name: str,
        embedding_model_name: str
    ):
        """
        Args:
            - ollama: Client to access Ollama.
            - db_path: Path to the data of the vector database.
            - collection_name: Name of the collection where documents will be
                saved.
            - embedding_model_name: Name of embedding model.
        """
        self._ollama = ollama
        self._db = chromadb.PersistentClient(path=db_path)
        self._collection_name = collection_name
        self._embedding_model_name = embedding_model_name

    def index_files(
        self,
        files_path: list[str],
        chunk_size: int = 1024,
        chunk_overlap: int = 20
    ):
        """Index files in the context.

        Args:
            - files_path: Path of each file to be indexed.
            - chunk_size: Size when splitting documents. The smaller,
                the more precise. More context at 
                https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
            - chunk_overlap: Amount of overlap when splitting documents into chunk_size.
        """

        documents = self._load_documents(files_path)

        if len(documents) == 0:
            raise AssertionError('No documents were loaded.')

        chunks = self._split_documents(documents, chunk_size, chunk_overlap)
        self._save_documents(chunks)

    def query(self, prompt: str, similarity_top_k: int = 4) -> str:
        """Query the context.

        Args:
            - prompt: Prompt to query the context.
            - top-k-results: How many chunks to return.

        Returns:
            Context found or empty string.
        """

        logger.info('m=query top_k:%d prompt=%s', similarity_top_k, prompt)

        embeddings = self._get_embeddings(prompt)
        collection = self._get_or_create_collection()
        results = collection.query(
            query_embeddings=[embeddings],
            n_results=similarity_top_k
        )

        context = ''
        for idx_doc, document in enumerate(results['documents']):
            for idx_chunk, chunk in enumerate(document):
                chunk_id = results['ids'][idx_doc][idx_chunk]
                context += f"<< Context {chunk_id} >>\n{chunk}\n\n"

        return context

    def _get_or_create_collection(self) -> Collection:
        return self._db.create_collection(
            name=self._collection_name,
            get_or_create=True,
            metadata={'hnsw:space': 'cosine'}
        )

    def _get_embeddings(self, text: str) -> Sequence[float]:
        response = self._ollama.embeddings(
            model=self._embedding_model_name,
            prompt=text,
        )
        return response['embedding']

    def _load_documents(self, files_path: list[str]) -> list[Document]:
        reader = SimpleDirectoryReader(
            input_files=files_path,
            exclude_hidden=False,
            recursive=True
        )
        documents = reader.load_data()
        logger.info('m=documents size=%d', len(documents))

        return documents

    def _split_documents(
        self,
        documents: list[Document],
        chunk_size: int,
        chunk_overlap: int
    ) -> list[BaseNode]:
        text_splitter = SentenceSplitter.from_defaults(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        nodes = text_splitter.get_nodes_from_documents(documents)
        logger.info('m=split size=%d overlap=%d len=%d',
                    chunk_size, chunk_overlap, len(nodes))

        return nodes

    def _save_documents(self, chunks: list[BaseNode]):
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            file_name = chunk.metadata['file_name']
            chunk_index = index

            chunk_id = f"{file_name}:{chunk_index}"
            document = chunk.get_content()
            embedding = self._get_embeddings(document)
            metadata = {
                'file-name': file_name,
                'chunk-index': chunk_index
            }

            ids.append(chunk_id)
            embeddings.append(embedding)
            documents.append(document)
            metadatas.append(metadata)

        collection = self._get_or_create_collection()
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
