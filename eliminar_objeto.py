import json
import boto3

def lambda_handler(event, context):
    # esperamos un JSON: { "bucket": "...", "key": "ruta/del/objeto" }
    body = json.loads(event.get('body', '{}'))
    bucket = body.get('bucket')
    key    = body.get('key')
    if not bucket or not key:
        return {'statusCode': 400, 'error': 'Faltan "bucket" o "key" en el body'}

    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {
        'statusCode': 200,
        'message': f'Objeto "{key}" eliminado de "{bucket}"'
    }
