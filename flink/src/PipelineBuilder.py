class PipelineBuilder:
    @staticmethod
    def build_validated_view(dataset, json_args):
        return f"validated_{dataset}_view", f"""
            SELECT *, 
                   validate_contract('{dataset}', JSON_OBJECT({json_args})) as is_valid
            FROM default_catalog.default_database.{dataset}_source
        """

    @staticmethod
    def build_main_insert(dataset, view_name, col_names_str):
        return f"""
            INSERT INTO paimon_catalog.paimon_db.{dataset}_sink 
            SELECT {col_names_str}, CURRENT_TIMESTAMP as _ingestion_ts 
            FROM {view_name}
            WHERE is_valid = TRUE
        """

    @staticmethod
    def build_dlq_insert(dataset, view_name, col_names_str):
        return f"""
            INSERT INTO paimon_catalog.paimon_db.{dataset}_dlq_sink
            SELECT 
                {col_names_str},
                CAST('Contract Violation' AS STRING) as _error_reason,
                CURRENT_TIMESTAMP as _ingestion_ts
            FROM {view_name}
            WHERE is_valid = FALSE
        """
