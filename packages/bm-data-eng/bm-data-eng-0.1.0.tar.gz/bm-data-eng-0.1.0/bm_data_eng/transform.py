from io import BytesIO

import pandas as pd


def transform_blob(
        gcs, bucket, source_key, dest_key, transformers):
    source_blob = gcs.get_bucket(bucket).blob(source_key)
    source_obj = source_blob.download()
    for t in transformers:
        source_obj = t(source_obj)
    target_blob = gcs.get_bucket(bucket).blob(dest_key)
    target_blob.upload_from_bytes(source_obj)


def csv_to_parquet(obj):
    df = pd.read_csv(BytesIO(obj))
    output = BytesIO()
    df.to_parquet(output)
    return output
