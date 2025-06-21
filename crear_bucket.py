import json
import boto3

def lambda_handler(event, context):
    # parseamos el body entrante
    try:
        body = json.loads(event.get('body', '{}'))
        bucket_name = body['bucket']
    except (json.JSONDecodeError, KeyError):
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Debe enviar JSON con el campo "bucket"'})
        }

    s3 = boto3.client('s3')
    try:
        # Si tu región no es us-east-1, quizá necesites esto:
        # s3.create_bucket(Bucket=bucket_name,
        #                  CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

    # Respuesta válida para API Gateway proxy
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'message': f'Bucket "{bucket_name}" creado con éxito'
        })
    }
