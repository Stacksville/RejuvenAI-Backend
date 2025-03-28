import pytest
from populate import load_knowledge_base


def test_load_knowledge_base_invalid_dataset(): 
    with pytest.raises(KeyError): 
        _ = load_knowledge_base("RANDOM_VAL")


def test_vdb_loads_successfully(): 
    pass

def record_manager_loads_successfully(): 
    pass

def validate_file_indexes(): 
    pass
