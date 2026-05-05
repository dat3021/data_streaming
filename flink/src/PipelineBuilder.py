class PipelineBuilder:
    @staticmethod
    def build_validated_view(dataset, json_args):
        """Creates a view that pre-calculates the validation result"""
        return f"validated_{dataset}_view", f"""
            SELECT *, 
                   validate_contract('{dataset}', JSON_OBJECT({json_args})) as is_valid
            FROM default_catalog.default_database.{dataset}_source
        """

    @staticmethod
    def build_main_insert(dataset, view_name, col_names_str):
        """SQL for good records - includes ingestion timestamp"""
        return f"""
            INSERT INTO paimon_catalog.paimon_db.{dataset}_sink 
            SELECT {col_names_str}, CURRENT_TIMESTAMP as _ingestion_ts 
            FROM {view_name}
            WHERE is_valid = TRUE
        """

    @staticmethod
    def build_dlq_insert(dataset, view_name, col_names_str):
        """
        SQL for bad records.
        Sinks to a dataset-specific Avro folder on S3 using Paimon engine.
        """
        return f"""
            INSERT INTO paimon_catalog.paimon_db.{dataset}_dlq_sink
            SELECT 
                {col_names_str},
                CAST('Contract Violation' AS STRING) as _error_reason,
                CURRENT_TIMESTAMP as _ingestion_ts
            FROM {view_name}
            WHERE is_valid = FALSE
        """
