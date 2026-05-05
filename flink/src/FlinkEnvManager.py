from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

class FlinkEnvManager:
    @staticmethod
    def setup_table_env():
        env = StreamExecutionEnvironment.get_execution_environment()
        settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
        t_env = StreamTableEnvironment.create(env, environment_settings=settings)
        
        env.enable_checkpointing(10000)
        t_env.get_config().set("table.exec.sink.upsert-materialize", "NONE")
        t_env.add_python_file("/opt/flink/usrlib/src")
        
        return t_env

    @staticmethod
    def register_metadata(t_env, validate_record_udf):
        t_env.execute_sql("""
            CREATE CATALOG paimon_catalog WITH (
                'type' = 'paimon',
                'warehouse' = 's3://data-streaming-pj/flink'
            )
        """)
        t_env.execute_sql("CREATE DATABASE IF NOT EXISTS paimon_catalog.paimon_db")
        t_env.create_temporary_system_function("validate_contract", validate_record_udf)
