import pytest
from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from populate import load_knowledge_base

def process_single_pdf(datasource_path: str): 
    dir = Path(datasource_path)
    path = dir.joinpath("bfw.pdf")
    print(f"reading {path}")
    loader = PyMuPDFLoader(path, mode='single')
    docs = loader.load()

    with open('extract.txt', 'a') as f: 
        for doc in docs: 
            f.writelines(doc.page_content)

    print("wrote file")


def test_load_knowledge_base_invalid_dataset(): 
    with pytest.raises(KeyError): 
        _ = load_knowledge_base("RANDOM_VAL")


def test_vdb_loads_successfully(): 
    pass

def record_manager_loads_successfully(): 
    pass

def validate_file_indexes(): 
    pass
