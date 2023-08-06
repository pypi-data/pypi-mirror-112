from io import BytesIO

import pandas as pd


def transform_blob(
        gcs, bucket, source_key, dest_key, transformers):
    print(
        f'In GCS bucket {bucket}, applying {len(transformers)} transformers to key '
        f'{source_key}, saving result in key {dest_key}...')
    source_blob = gcs.get_bucket(bucket).blob(source_key)
    source_obj = source_blob.download_as_string()
    for t in transformers:
        source_obj = t(source_obj)
    target_blob = gcs.get_bucket(bucket).blob(dest_key)
    target_blob.upload_from_string(source_obj)
    print('Done.')


def csv_to_parquet(obj):
    df = pd.read_csv(BytesIO(obj))
    buffer = BytesIO()
    df.to_parquet(buffer)
    return buffer.getvalue()
