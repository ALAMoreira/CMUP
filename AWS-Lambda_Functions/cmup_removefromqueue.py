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
        return {
            'statusCode': 200,
            'body': json.dumps('There is no user in ' + restaurant +"'s queue!")
        }

    item = response['Item']

    queued = OrderedDict(item)
    queued = list(item.items())

    found = False
    queue_position = 0
    for i in queued:
        if 'restaurant' in i:
            continue
        queue_position = queue_position + 1
        if user in item[i[0]]:
            found = True
            break

    if found:
        for n in range(queue_position, len(item)):
            # print('n: ' + str(n) + ' length: ' + str(len(item) - 1))
            if not n == len(item) - 1:
                item['queue:' + str(n)] = item['queue:' + str(n + 1)]
            else:
                item.pop('queue:' + str(n))

    if len(item) - 1 == 0:
        table_queue.delete_item(
            Key={
                'restaurant': restaurant
            }
        )
    else:
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

    if 'restaurant' in item:
        item.pop('restaurant')

    table.put_item(
        Item=item
    )

    return {
        'statusCode': 200,
        'body': json.dumps('User ' + user + ' removed from ' + restaurant + "'s queue!")
    }