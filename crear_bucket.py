import json
import boto3

def lambda_handler(event, context):
    # esperamos un JSON: { "bucket": "nombre-que-quieras" }
    body = json.loads(event.get('body', '{}'))
    bucket_name = body.get('bucket')
    if not bucket_name:
        return {'statusCode': 400, 'error': 'Falta el parámetro "bucket" en el body'}

    s3 = boto3.client('s3')
    try:
        # Si estás fuera de us-east-1 quizá necesites CreateBucketConfiguration
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {
        'statusCode': 200,
        'message': f'Bucket "{bucket_name}" creado con éxito'
    }
