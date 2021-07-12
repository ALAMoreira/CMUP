import boto3, json
from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')
table_queue = dynamodb.Table('cmup_restaurant_queue')

def lambda_handler(event, context):

    restaurant = event['queryStringParameters']['restaurant']
    user = event['queryStringParameters']['user']

    # Add user to queue
    response = table_queue.get_item(
        Key={
            'restaurant': restaurant
        }
    )

    if not 'Item' in response:
        response['Item'] = {}

    item = response['Item']

    queue_size = len(item)
    queued = OrderedDict(item)
    queued = list(item.items())

    found = False
    if queue_size == 0:
        item['restaurant'] = restaurant
        item['queue:1'] = user
    else:
        for i in queued[1]:
            if user in i:
                print(i)
                found = True
                break
        if not found:
            item['queue:' + str(queue_size)] = user
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('User ' + user + ' already in ' + restaurant + "'s queue!")
            }

    table_queue.put_item(
        Item=item
    )

    # Update restaurant info on user
    response = table.get_item(
        Key={
            'id': user
        }
    )

    item = response['Item']

    item['restaurant'] = restaurant

    table.put_item(
        Item=item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('User ' + user + ' added to ' + restaurant + "'s queue!")
    }