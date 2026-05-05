import os
import yaml
import sys

sys.path.append("/opt/flink/usrlib/src")

from DataContracValidator import validate_record
from PipelineBuilder import PipelineBuilder
from FlinkEnvManager import FlinkEnvManager

def run_pipelines():
    # 1. Setup Environment and Metadata
    t_env = FlinkEnvManager.setup_table_env()
    FlinkEnvManager.register_metadata(t_env, validate_record)
    
    # 2. Build Pipeline
    query_dir = "/opt/flink/usrlib/src/queries"
    stmt_set = t_env.create_statement_set()
    
    for filename in os.listdir(query_dir):
        if filename.endswith(".yml"):
            with open(os.path.join(query_dir, filename), 'r') as f:
                config = yaml.safe_load(f)
                dataset = config['dataset']
                
                # 3. Register All Tables (Source, Main Sink, DLQ Sink)
                t_env.execute_sql(config['source_ddl'])
                t_env.execute_sql(config['sink_ddl'])
                t_env.execute_sql(config['dlq_sink_ddl'])
                
                # 4. Prepare Schema and JSON args for validation UDF
                source_path = f"default_catalog.default_database.{dataset}_source"
                col_names = t_env.from_path(source_path).get_schema().get_field_names()
                col_names_str = ", ".join(col_names)
                json_args = ", ".join([f"KEY '{c}' VALUE {c}" for c in col_names])
                
                # 5. Create Validation View (Ensures UDF runs only once per row)
                view_name, view_sql = PipelineBuilder.build_validated_view(dataset, json_args)
                t_env.create_temporary_view(view_name, t_env.sql_query(view_sql))
                
                # 6. Add Main and DLQ streams to the unified job (StatementSet)
                stmt_set.add_insert_sql(PipelineBuilder.build_main_insert(dataset, view_name, col_names_str))
                stmt_set.add_insert_sql(PipelineBuilder.build_dlq_insert(dataset, view_name, col_names_str))

    # 7. Execute all pipelines as a single Flink Job
    stmt_set.execute()

if __name__ == "__main__":
    run_pipelines()
