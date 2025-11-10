import json

from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import JSONLoader, PyPDFLoader, NotebookLoader, CSVLoader

class SimpleJSONLLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        docs = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    docs.append(Document(
                        page_content=obj["page_content"],
                        metadata=obj.get("metadata", {})
                    ))
        return docs

def load_data(data_dir: str):
    data_path = Path(data_dir).resolve()
    print(f'Data Path: {data_dir}')
    docs = []

    # PDF Files
    pdf_files = list(data_path.glob('**/*.pdf'))
    print(f'Found {len(pdf_files)} PDF files: {[str(f) for f in pdf_files]}')
    for file in pdf_files:
        print(f'Loading PDF {file}')
        try:
            loader = PyPDFLoader(str(file))
            loaded = loader.load()
            for page in loaded:
                page.metadata['source_file'] = file.name
                page.metadata['file_type'] = 'pdf'
            print(f'Loaded PDF: {file}')
            docs.extend(loaded)
        except Exception as e:
            print(f'Cound not load PDF : {file}, {e}')
            raise

    # JSON
    json_files = list(data_path.glob('**/*.json'))
    print(f'Found {len(json_files)} JSON files: {[str(f) for f in json_files]}')
    for file in json_files:
        print(f'Loading JSON {file}')
        # Try JSONL first
        try:
            loader = SimpleJSONLLoader(file)
            loaded = loader.load()
            if len(loaded) > 1:
                print(f"Loaded {len(loaded)} JSONL documents: {file}")
                for d in loaded:
                    d.metadata['source_file'] = Path(file).name
                    d.metadata['file_type'] = 'jsonl'
                docs.extend(loaded)
                continue  # SUCCESS → skip JSON fallback
        except Exception as e:
            print(f"JSONL load failed, trying normal JSON: {e}")

        try:
            # loader = JSONLoader(
            #     file_path=file,
            #     jq_schema='.',
            #     text_content=False
            # )
            loader = JSONLinesLoader(str(file))
            loaded = loader.load()
            for page in loaded:
                page.metadata['source_file'] = file.name
                page.metadata['file_type'] = 'json'
            print(f'Loaded JSON: {file}')
            docs.extend(loaded)
        except Exception as e:
            print(f'Cound not load JSON : {file}, {e}')
            raise
    
    # IPYNB
    notebook_files = list(data_path.glob('**/*.ipynb'))
    print(f'Found {len(notebook_files)} ipynb files: {[str(f) for f in notebook_files]}')
    for file in notebook_files:
        print(f'Loading ipynb {file}')
        try:
            # loader = NotebookLoader(
            #     file,
            #     include_outputs=True,
            #     max_output_length=1000,
            #     remove_newline=True,
            # )
            loader = NotebookLoader(str(file))
            loaded = loader.load()
            for page in loaded:
                page.metadata['source_file'] = file.name
                page.metadata['file_type'] = 'ipynb'
            print(f'Loaded ipynb: {file}')
            docs.extend(loaded)
        except Exception as e:
            print(f'Cound not load ipynb : {file}, {e}')
            raise
    
    # CSV
    csv_files = list(data_path.glob('**/*.csv'))
    print(f'Found {len(csv_files)} CSV files: {[str(f) for f in csv_files]}')
    for file in csv_files:
        print(f'Loading CSV {file}')
        try:
            # loader = CSVLoader(
            #     file_path=file,
            #     csv_args={
            #         'delimiter': ',',
            #         'quotechar': '"',
            #     },
            #     encoding='latin-1'
            # )
            loader = CSVLoader(str(file))
            loaded = loader.load()
            for page in loaded:
                page.metadata['source_file'] = file.name
                page.metadata['file_type'] = 'csv'
            print(f'Loaded CSV: {file}')
            docs.extend(loaded)
        except Exception as e:
            print(f'Cound not load CSV : {file}, {e}')
            raise

    return docs