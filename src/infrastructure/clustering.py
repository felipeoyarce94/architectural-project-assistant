"""This module contains the implementation of the Clustering protocol."""

import PyPDF2 
import logging
import numpy as np
import re
from langchain.embeddings import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from src.settings import TEXT_EMBEDDING_MODEL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_sentences(file_path: str) -> list[dict[str, int | str]]:
    """
    This function reads a PDF file and returns a list of sentences.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        list[dict]: The list of sentences with their index.
    """
    try:
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            single_sentences_list = re.split(r'(?<=[.?!])\s+', text)
            sentences = [{'sentence': x, 'index' : i} for i, x in enumerate(single_sentences_list)]
            logging.info(f"Extracted {len(sentences)} sentences from {file_path}")
            return sentences
    except Exception as e:
        logging.error(f"Error reading PDF file: {e}")
        return []
    
def combine_sentences(sentences: list[dict[str, int | str]], buffer_size=1) -> list[dict[str, int | str]]:
    """
    This function combines the sentences into a single string.
    """
    # Go through each sentence dict
    logging.info(f"Combining {len(sentences)} sentences")
    for i in range(len(sentences)):

        # Create a string that will hold the sentences which are joined
        combined_sentence = ''

        # Add sentences before the current one, based on the buffer size.
        for j in range(i - buffer_size, i):
            # Check if the index j is not negative (to avoid index out of range like on the first one)
            if j >= 0:
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += sentences[j]['sentence'] + ' '

        # Add the current sentence
        combined_sentence += sentences[i]['sentence']

        # Add sentences after the current one, based on the buffer size
        for j in range(i + 1, i + 1 + buffer_size):
            # Check if the index j is within the range of the sentences list
            if j < len(sentences):
                # Add the sentence at index j to the combined_sentence string
                combined_sentence += ' ' + sentences[j]['sentence']

        # Then add the whole thing to your dict
        # Store the combined sentence in the current sentence dict
        sentences[i]['combined_sentence'] = combined_sentence

    return sentences

def calculate_similarity(sentences: list[dict[str, int | str]]) -> tuple[list[float], list[dict[str, int | str]]]:
    """
    This function calculates the similarity between two sentences.
    """
    logging.info(f"Calculating embeddings for {len(sentences)} sentences")
    oaiembeds = OpenAIEmbeddings(model=TEXT_EMBEDDING_MODEL)
    embeddings = oaiembeds.embed_documents([x['combined_sentence'] for x in sentences])
    logging.info(f"Embeddings calculated for {len(sentences)} sentences")
    for i, sentence in enumerate(sentences):
        sentence['combined_sentence_embedding'] = embeddings[i]
    logging.info(f"Calculating distances for {len(sentences)} sentences")
    distances = []
    for i in range(len(sentences) - 1):
        embedding_current = sentences[i]['combined_sentence_embedding']
        embedding_next = sentences[i + 1]['combined_sentence_embedding']
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]
        
        # Convert to cosine distance
        distance = 1 - similarity

        # Append cosine distance to the list
        distances.append(distance)

        # Store distance in the dictionary
        sentences[i]['distance_to_next'] = distance

    # Optionally handle the last sentence
    # sentences[-1]['distance_to_next'] = None  # or a default value
    logging.info(f"Distances calculated for {len(sentences)} sentences")
    return distances, sentences

def create_semantic_chunks(sentences: list, distances: list, percentile_threshold: int = 95) -> list:
    """
    Creates semantic chunks from sentences based on cosine distances.
    
    Args:
        sentences (list): List of dictionaries containing sentence data
        distances (list): List of cosine distances between consecutive sentences
        percentile_threshold (int): Percentile threshold for chunk breakpoints (default: 95)
    
    Returns:
        list: List of text chunks where each chunk contains semantically related sentences
    """
    # Calculate distance threshold based on percentile
    breakpoint_distance_threshold = np.percentile(distances, percentile_threshold)
    
    # Get indices where distance exceeds threshold
    indices_above_thresh = [
        i for i, x in enumerate(distances) 
        if x > breakpoint_distance_threshold
    ]
    
    chunks = []
    start_index = 0
    
    # Create chunks based on breakpoints
    for index in indices_above_thresh:
        group = sentences[start_index:index + 1]
        combined_text = ' '.join([d['sentence'] for d in group])
        chunks.append(combined_text)
        start_index = index + 1
    
    # Add remaining sentences as final chunk
    if start_index < len(sentences):
        combined_text = ' '.join([d['sentence'] for d in sentences[start_index:]])
        chunks.append(combined_text)
        
    return chunks
