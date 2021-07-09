import boto3, json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')

def lambda_handler(event, context):

    response = table.scan(
        FilterExpression=Attr('restaurant').eq(event['pathParameters']['restaurant'])
    )

    # items = response['Items']

    users = []
    for i in response['Items']:
        users.append(i['id'])

    return {
        'statusCode': 200,
        'body': json.dumps(str(set(users)))
    }