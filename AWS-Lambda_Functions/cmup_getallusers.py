import boto3, json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')

def lambda_handler(event, context):

    response = table.scan()

    users = {}
    for i in response['Items']:
        users[i['id']] = i

    return {
        'statusCode': 200,
        'body': json.dumps(users)
    }
