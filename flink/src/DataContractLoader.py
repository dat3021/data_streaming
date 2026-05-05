import os
import yaml
from typing import Dict, Any

class DataContractLoader:
    """Helper class to load and manage Data Contracts from YAML files."""
    
    def __init__(self, contract_dir: str = "../data-contract"):
        self.contract_dir = contract_dir
        self.contracts: Dict[str, Any] = {}
        self.load_all()

    def load_all(self):
        """Scan directory and load all .yml files."""
        if not os.path.exists(self.contract_dir):
            print(f"Warning: Contract directory {self.contract_dir} not found.")
            return

        for filename in os.listdir(self.contract_dir):
            if filename.endswith(".yml") or filename.endswith(".yaml"):
                path = os.path.join(self.contract_dir, filename)
                with open(path, 'r') as f:
                    config = yaml.safe_load(f)
                    dataset = config.get('dataset')
                    if dataset:
                        self.contracts[dataset] = config
                        print(f"Loaded contract for dataset: {dataset}")

    def get_contract(self, dataset: str) -> Dict[str, Any]:
        """Retrieve a specific contract."""
        return self.contracts.get(dataset)
