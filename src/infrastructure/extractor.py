from langchain_community.document_loaders import PyPDFLoader
from src.models import Item
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableSerializable
import logging
from src.settings import DEFAULT_MODEL
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Extractor:
    """
    This class is used to extract the Items from a PDF document using a prompt.
    
    It uses the ChatOpenAI model to extract the Items from the PDF document.
    
    
    Args:
        prompt_path (str): The path to the prompt file.
    
    Returns:
        list[Item]: The list of extracted items.
    """
    def __init__(self, prompt_path: str):
        self.prompt_path = prompt_path
        
        try:
            self.gpt_model = ChatOpenAI(model=DEFAULT_MODEL)
        except Exception as e:
            logging.error(f"Failed to initialize ChatOpenAI: {e}")
            raise

        try:
            with open(self.prompt_path, "r") as f:
                self.extraction_prompt_text = f.read()
            self.extraction_prompt = ChatPromptTemplate.from_template(self.extraction_prompt_text)
        except FileNotFoundError:
            logging.error(f"Prompt file not found: {self.prompt_path}")
            raise
        except Exception as e:
            logging.error(f"Error reading prompt file: {e}")
            raise

    def _load_pdf(self, file_path: str) -> list[Document]:
        """
        Loads the PDF file and returns a list of documents.
        
        Args:
            file_path (str): The path to the PDF file.
            
        Returns:
            list[Document]: The list of documents.
        """
        try:
            loader = PyPDFLoader(file_path=file_path)
            documents: list[Document] = loader.load()
            logging.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents
        except Exception as e:
            logging.error(f"Failed to load PDF {file_path}: {e}")
            raise

    def extract_items(self, docs: list[Document]) -> list[Item]:
        """
        Extracts items from the provided documents.
        
        Args:
            docs (list[Document]): The list of documents to extract items from.
            
        Returns:
            list[Item]: The list of extracted items.
        """
        if not docs:
            logging.warning("No documents provided for extraction")
            return []

        logging.info(f"Starting extraction from {len(docs)} documents")
        
        question_chain: RunnableSerializable = (
            {"context": RunnablePassthrough()}
            | self.extraction_prompt
            | self.gpt_model.with_structured_output(Item)
        )

        extracted_items: list[Item] = []
        for i, doc in enumerate(docs, 1):
            try:
                item = question_chain.invoke({"context": doc})
                extracted_items.append(item)
                logging.info(f"Processed document {i}/{len(docs)}")
            except Exception as e:
                logging.error(f"Failed to extract from document {i}: {e}")
                continue

        logging.info(f"Successfully extracted {len(extracted_items)} items")
        return extracted_items
