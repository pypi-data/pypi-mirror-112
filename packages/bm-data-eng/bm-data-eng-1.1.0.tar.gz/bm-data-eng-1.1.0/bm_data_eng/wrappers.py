from google.cloud import bigquery

from bm_data_eng.s3_to_gcs import gcs_uri
from bm_data_eng.transform import transform_blob
from bm_data_eng.bigquery import load_to_bq


def transform_and_load(
        gcs, bucket, raw_key, transformed_key, transformers, bq, dest_table,
        job_config):
    transform_blob(gcs, bucket, raw_key, transformed_key, transformers)
    dest_table = bigquery.table.TableReference.from_string(dest_table)
    load_result = load_to_bq([gcs_uri(bucket, transformed_key)], bq, dest_table, job_config)
    print(load_result.state)
