import json


def lambda_handler(event, context):
    req_body = json.loads(event['body'].encode('utf-8'))
    image_string = req_body.get('image')
    if image_string == 'trigger':
        return {
            'statusCode': 200,
            'body': json.dumps(
                {
                    'predicted': 'trigger successful',
                }
            )
        }