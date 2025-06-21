import json
import boto3

def lambda_handler(event, context):
    # parseamos el body entrante
    try:
        body = json.loads(event.get('body', '{}'))
        bucket = body['bucket']
        key    = body['key']
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Debe enviar JSON con "bucket" y "key"'})
        }

    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'message': f'Objeto "{key}" eliminado de "{bucket}"'})
    }
