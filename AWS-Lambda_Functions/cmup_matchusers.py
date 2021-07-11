import boto3, json
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
# from scipy import pandas
# from pyspark.sql import *

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cmup_users')


def lambda_handler(event, context):

    response = table.scan(
        FilterExpression=Attr('restaurant').eq(event['pathParameters']['restaurant'])
    )

    # items = response['Items']

    # users = []
    # for i in response['Items']:
    #     users.append(i['id'])

    interests = {}
    user_interests = {}

    for n in response['Items']:
        # print(n)
        user_id = n['id']
        # print('----------------------\n' + user_id)
        for key, value in n.items():
            if 'interest' in key.lower():
                user_interests[value] = 1
        interests[user_id] = user_interests
        user_interests = {}

    print(interests)

    # df = pd.DataFrame.from_dict(interests)
    # df.fillna(0)

    return {
        'statusCode': 200,
        'body': json.dumps(str(interests))
    }


    # from sklearn.metrics import jaccard_score
    # A = [1, 1, 1, 0]
    # B = [1, 1, 0, 1]
    # jacc = jaccard_score(A,B)
    # print(‘Jaccard similarity: %.3f’ % jacc)