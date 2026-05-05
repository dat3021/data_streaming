import json
import re
from pyflink.table.udf import ScalarFunction, udf
from pyflink.table import DataTypes
from DataContractLoader import DataContractLoader

class DataContracValidator(ScalarFunction):
    """
    Flink UDF to validate incoming records against Data Contracts.
    Returns True if valid, False otherwise.
    """

    def __init__(self):
        self.loader = None

    def open(self, function_context):
        """Initialize loader once per TaskManager execution."""
        self.loader = DataContractLoader(contract_dir="/opt/flink/usrlib/data-contract")

    def eval(self, dataset_name: str, record_json: str) -> bool:
        """
        Main validation logic.
        :param dataset_name: The name of the dataset
        :param record_json: The row data serialized as a JSON string
        """
        contract = self.loader.get_contract(dataset_name)
        if not contract:
            return True 

        try:
            record_dict = json.loads(record_json)
        except Exception as e:
            print(f"JSON Parse Error for {dataset_name}: {e}")
            return False

        # 1. Schema Validation
        for schema_item in contract.get('schema', []):
            col = schema_item['column']
            val = record_dict.get(col)
            
            constraints = schema_item.get('constraints', [])
            if 'not_null' in constraints and val is None:
                print(f"Validation Failed: {col} is null for {dataset_name}")
                return False
            
            for constraint in constraints:
                if isinstance(constraint, dict) and 'pattern' in constraint:
                    if not re.match(constraint['pattern'], str(val or "")):
                        print(f"Validation Failed: {col} does not match pattern for {dataset_name}")
                        return False

        # 2. Quality Rules Validation
        for rule in contract.get('quality_rules', []):
            col = rule['column']
            val = record_dict.get(col)
            
            # Skip quality rule if value is None (caught by not_null if required)
            if val is None:
                continue
                
            if rule['expectation'] == 'expect_column_values_to_be_greater_than_or_equal_to':
                if not (val >= rule['value']):
                    print(f"Validation Failed: {col} < {rule['value']} for {dataset_name}")
                    return False
            
            elif rule['expectation'] == 'expect_column_values_to_be_greater_than':
                if not (val > rule['value']):
                    print(f"Validation Failed: {col} <= {rule['value']} for {dataset_name}")
                    return False

        return True

# Helper to define the UDF with strict PyFlink types
validate_record = udf(DataContracValidator(), 
                      input_types=[DataTypes.STRING(), DataTypes.STRING()],
                      result_type=DataTypes.BOOLEAN())
