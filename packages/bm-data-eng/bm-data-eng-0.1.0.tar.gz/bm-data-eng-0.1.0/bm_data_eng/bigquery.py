def load_to_bq(source_uris, bq, dest_table, job_config):
    return bq.load_table_from_uri(source_uris, dest_table, job_config=job_config).result()
