def transfer_to_gcs(
        s3, s3_bucket, s3_key, gcs, gcs_bucket, gcs_key):
    print(f'Transferring object from: S3, bucket {s3_bucket}, key {s3_key}.')
    print(f'Transferring to GCS, bucket {gcs_bucket}, key {gcs_key}...')
    source_obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)['Body'].read()
    target_blob = gcs.get_bucket(gcs_bucket).blob(gcs_key)
    target_blob.upload_from_string(source_obj)
    print('Done')


def gcs_uri(bucket, key):
    return f'gs://{bucket}/{strip_slash(key)}'


def strip_slash(s):
    return s if not s.startswith('/') else s[1:]
