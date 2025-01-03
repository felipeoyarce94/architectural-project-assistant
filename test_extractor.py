import logging
import json
from datetime import datetime
from pathlib import Path
from src.infrastructure.extractor import Extractor
from src.settings import DEFAULT_FILE_PATH, DEFAULT_PROMPT_PATH, DEFAULT_MODEL
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_to_json(items, output_dir="output"):
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"extracted_items_{timestamp}.json"
    filepath = Path(output_dir) / filename
    
    # Convert items to dictionary format
    items_dict = [item.model_dump() for item in items]
    
    # Save to JSON file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(items_dict, f, indent=2, ensure_ascii=False)
        logging.info(f"Successfully saved results to {filepath}")
        return filepath
    except Exception as e:
        logging.error(f"Failed to save results: {e}")
        raise

def main():
    # Initialize the extractor with your configurations
    extractor = Extractor(
        file_path=DEFAULT_FILE_PATH,
        prompt_path=DEFAULT_PROMPT_PATH,
        model=DEFAULT_MODEL
    )
    
    try:
        # Load the PDF documents
        documents = extractor._load_pdf()
        
        # Extract items from the documents
        items = extractor.extract_items(documents)
        
        # Save results to JSON
        output_file = save_to_json(items)
        
        # Optional: Still print results to console
        for i, item in enumerate(items, 1):
            print(f"\nItem {i}:")
            print(f"Title: {item.title}")
            print(f"Description: {item.description}")
            
    except Exception as e:
        logging.error(f"Extraction failed: {e}")

if __name__ == "__main__":
    main()