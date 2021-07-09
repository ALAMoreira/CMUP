import boto3, json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')

def lambda_handler(event, context):

    response = table.scan()
    user_id = 'user' + str(len(response['Items']) + 1)

    attributes = {}
    attributes['id'] = user_id
    for key, value in event.items():
        attributes[key] = value

    table.put_item(Item=attributes)

    return {
        'statusCode': 200,
        'body': json.dumps('User created successfully!\n' + str(attributes))
    }