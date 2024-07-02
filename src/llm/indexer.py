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

    def index_files(self, files_path: list[str]):
        """Index files in the context.

        Args:
            - files_path: Path of each file to be indexed.
        """

        documents = self._load_documents(files_path)
        chunks = self._split_documents(documents)
        self._save_documents(chunks)

    def query(self, prompt: str, top_k_results: int = 4) -> str:
        """Query the context.

        Args:
            - prompt: Prompt to query the context.
            - top-k-results: How many chunks to return.

        Returns:
            Context found or empty string.
        """

        logger.info('m=query prompt=%s', prompt)

        embeddings = self._get_embeddings(prompt)
        collection = self._get_or_create_collection()
        results = collection.query(
            query_embeddings=[embeddings],
            n_results=top_k_results
        )

        context = ''
        for document in results['documents']:
            chunks = '\n\n'.join(document)
            context += chunks

        return context

    def _get_or_create_collection(self) -> Collection:
        """Get or create the database collection to manage vector data.

        Returns:
            The collection.
        """
        return self._db.create_collection(
            name=self._collection_name,
            get_or_create=True,
            metadata={'hnsw:space': 'cosine'}
        )

    def _get_embeddings(self, text: str) -> Sequence[float]:
        """Generate embeddings from a chunk of text.

        Returns
            Generate embeddings.
        """
        response = self._ollama.embeddings(
            model=self._embedding_model_name,
            prompt=text,
        )
        return response['embedding']

    def _load_documents(self, files_path: list[str]) -> list[Document]:
        """Load documents from a list of file paths.

        Args:
            - files_path: Path of each file to be loaded.

        Returns
            Documents loaded.
        """
        reader = SimpleDirectoryReader(
            input_files=files_path,
            exclude_hidden=False,
            recursive=True
        )
        documents = reader.load_data()
        logger.info('m=documents size=%d', len(documents))

        return documents

    def _split_documents(self, documents: list[Document]) -> list[BaseNode]:
        """Split documents into chunks

        Args:
            - documents: Documents to be splitted.

        Returns
            Nodes of the splitted documents.
        """

        text_splitter = SentenceSplitter.from_defaults(
            chunk_size=800,
            chunk_overlap=80,
        )
        nodes = text_splitter.get_nodes_from_documents(documents)
        logger.info('m=split size=%d', len(nodes))

        return nodes

    def _save_documents(self, chunks: list[BaseNode]):
        """Save documents in the database.

        Args:
            - chunks: Chunks of documents to be saved.
        """
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):
            file_name = chunk.metadata['file_name']
            page = chunk.metadata['page_label']
            chunk_index = index

            chunk_id = f"{file_name}:{page}-{chunk_index}"
            document = chunk.get_content()
            embedding = self._get_embeddings(document)
            metadata = {
                'file-name': file_name,
                'page': page,
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
