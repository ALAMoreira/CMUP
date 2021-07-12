import boto3, json
from boto3.dynamodb.conditions import Key, Attr
# from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')
table_queue = dynamodb.Table('cmup_restaurant_queue')

def lambda_handler(event, context):

    queue = {
        "queue:1": "user3",
        "queue:2": "user1",
        "queue:3": "user5",
        "restaurant": "meal&wine"
        }

    table_queue.put_item(
        Item=queue
    )

    response = table.scan(
        FilterExpression=Attr('matched').eq(True)
    )

    items = response['Items']

    for i in items:
        response = table.get_item(
            Key={
                'id': i['id']
            }
        )
        item = response['Item']

        item['matched'] = False

        table.put_item(
            Item=item
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Queue reseted sucessfully!')
    }