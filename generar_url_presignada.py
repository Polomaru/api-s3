import json
import boto3

def lambda_handler(event, context):
    # parseamos el body entrante
    try:
        body = json.loads(event.get('body', '{}'))
        bucket  = body['bucket']
        key     = body['key']
        expires = int(body.get('expires', 3600))
    except (json.JSONDecodeError, KeyError, ValueError):
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Debe enviar JSON con "bucket", "key" y opcionalmente "expires" (int)'
            })
        }

    s3 = boto3.client('s3')
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'presigned_url': url,
            'expires_in': expires
        })
    }
