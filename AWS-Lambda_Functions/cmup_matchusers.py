import boto3, json
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
# from scipy import pandas
# from pyspark.sql import *
from scipy.spatial.distance import pdist, squareform
import random

from collections import OrderedDict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')
table_queue = dynamodb.Table('cmup_restaurant_queue')


def lambda_handler(event, context):

    # Get queued users
    response = table_queue.get_item(
        Key={
            'restaurant': event['pathParameters']['restaurant']
        }
    )

    original_queue = response['Item']

    queued = OrderedDict(response['Item'])
    queued = list(queued.items())

    print(queued[-1][0])
    print(queued[1:])

    print(queued[0])

    # list(queued)[-1]

    # ---------------------------------------------

    # Update user's table
    # response = table.get_item(
    #     Key={
    #         'id': 'user1'
    #     }
    # )

    # item = response['Item']

    # item['table'] = random.randint(1, 10)

    # table.put_item(
    #   Item=item
    # )

    # ---------------------------------------------

    # # Check if there are matched users
    # response = table.scan(
    #     FilterExpression=Attr('matched').eq(True) & Attr('restaurant').eq(event['pathParameters']['restaurant'])
    # )
    # items = response['Items']
    # matched_count = len(items)
    # print('Matched: ' + str(matched_count))

    # is_match_possible = bool(matched_count % 2)
    # if is_match_possible is False:
    #     print('No one to match!')

    # ---------------------------------------------

    # Get users to match v2
    keys = []
    for i in queued[1:]:
        keys.append({'id': i[1]})

    print('keys : ' + str(keys))

    response = dynamodb.batch_get_item(
        RequestItems={
            'cmup_users':{
                'Keys': keys
            }
        }
    )

    items = response['Responses']['cmup_users']
    print(items)

    # ---------------------------------------------

    # # Get users to match
    # response = table.scan(
    #     FilterExpression=Attr('restaurant').eq(event['pathParameters']['restaurant'])
    # )

    # items = response['Items']

    # users = []
    # for i in response['Items']:
    #     users.append(i['id'])



    # ---------------------------------------------

    # Build interests table
    interests = {}
    user_interests = {}

    for n in items:
        # print(n)
        if n['matched'] is False:
            user_id = n['id']
            # print('----------------------\n' + user_id)
            for key, value in n.items():
                if 'interests' in key.lower():
                    user_interests[value] = 1
            interests[user_id] = user_interests
            user_interests = {}

    # print(interests)

    # df = pd.DataFrame.from_dict(interests)
    # df.fillna(0)

    df = pd.DataFrame.from_dict(interests)
    df = df.fillna(0)

    print(df)


    # ---------------------------------------------

    # Calculate Hamming Distance
    pairwise = 1 - pd.DataFrame(
        squareform(pdist(df.T, metric='hamming')),
        columns = df.columns,
        index = df.columns
    )

    for n in range(len(pairwise)):
        pairwise.iloc[n][n] = 0

    print(pairwise)

    # ---------------------------------------------

    # Match users
    user_match = {}
    count_index = 0
    for i in pairwise:
        max_value, count_column = 0, 0
        for z in pairwise.columns:
            if pairwise.iloc[count_index][count_column] > max_value:
                max_value = pairwise.iloc[count_index][count_column]
                # print(z)
                user_match[i] = {z: max_value}
            # print(count_column)
            count_column = count_column + 1
        count_index = count_index + 1

    print(user_match)

    matched_users = []
    for i in user_match.items():
        # print(i[1])
        user = i[0]
        if user in matched_users:
            print('continue')
            continue
        for z in i[1].items():
            # print(z[0])
            user_to_match = z[0]
            # Get user to match matched user and value
            matched_user = user_match[str(z[0])].items()
            # print('matched_user: ' + str(matched_user))
            matched_user = list(matched_user)[0][0]
            # If user to match matched user is the same as current user, then they've matched
            if bool(matched_user == user):
                # print('user_to_match: ' + user_to_match + ' - user: ' + user)
                matched_users.extend([user, user_to_match])
                # for n in items:
                #     if user in n['id'] or user_to_match in n['id']:
                #         n['matched'] = True
                #         # print('True - ' + n['id'] + ' - user ' + user + ' - user_to_match ' + user_to_match)
                #     # else:
                #         # print('False - ' + n['id'])

    # print('matched_users - ' + str(matched_users))
    print(items)

    # ---------------------------------------------

    # Update matched values on matched users

    # keys = []
    # for i in matched_users:
    #     keys.append({'id': i})

    # print('keys : ' + str(keys))

    for i in matched_users:
        response = table.get_item(
            Key={
                'id': i
            }
        )
        item = response['Item']

        item['matched'] = True

        table.put_item(
        Item=item
        )

    # ---------------------------------------------

    # Remove users and update queue
    new_queue = {}
    queue_count = 0
    users_in_queue = []
    for n in original_queue:
        if 'restaurant' in n:
            new_queue[n] = original_queue[n]
            continue
        if not original_queue[n] in matched_users:
            queue_count = queue_count + 1
            new_queue[str('queue:' + str(queue_count))] = original_queue[n]
            users_in_queue.append(original_queue[n])

    print('New queue ' + str(new_queue))

    table_queue.put_item(
        Item=new_queue
    )

    # from sklearn.metrics.pairwise import pairwise_distances

    # jac_sim = 1 - pairwise_distances(df.T, metric = "hamming")
    # jac_sim = pd.DataFrame(jac_sim, index=df.columns, columns=df.columns)

    # print(jac_sim)

    return {
        'statusCode': 200,
        'body': json.dumps('Matched users: ' + str(matched_users) + ' - Users in queue: ' + str(users_in_queue))
    }