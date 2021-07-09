import boto3, json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')

def lambda_handler(event, context):

    response = table.get_item(
        Key={
            'id': event['pathParameters']['user']
        }
    )

    user = response['Item']

    return {
        'statusCode': 200,
        'body': json.dumps(user)
    }
