import json
import boto3

def lambda_handler(event, context):
    # esperamos un JSON: { "bucket": "...", "key": "...", "expires": 3600 }
    body = json.loads(event.get('body', '{}'))
    bucket  = body.get('bucket')
    key     = body.get('key')
    expires = int(body.get('expires', 3600))  # segundos

    if not bucket or not key:
        return {'statusCode': 400, 'error': 'Faltan "bucket" o "key" en el body'}

    s3 = boto3.client('s3')
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires
        )
    except Exception as e:
        return {'statusCode': 500, 'error': str(e)}

    return {
        'statusCode': 200,
        'presigned_url': url,
        'expires_in': expires
    }
