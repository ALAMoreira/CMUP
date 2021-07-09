import boto3, json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')

def lambda_handler(event, context):

    response = table.scan()

    restaurants = []
    for i in response['Items']:
        if 'restaurant' in i:
            restaurants.append(i['restaurant'])

    return {
        'statusCode': 200,
        'body': json.dumps(str(set(restaurants)))
    }
