import boto3
from boto3.dynamodb.conditions import Key, Attr

# This helper will query all the items with 'partkey'
# and having 'id_field' = ids
table_name = 'your_table'
partkey = 'your_part_key'
id_field = 'id_'
ids = ['id1', 'id2']

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


def query_all_items(key_condition_expression, filter_expression=None,
                    projection_expression=None, table=table, index_name=None,
                    expr_attr_names=None):
    

    kwargs = {'KeyConditionExpression': key_condition_expression}

    if filter_expression:
        kwargs.update({'FilterExpression': filter_expression})

    if projection_expression:
        kwargs.update({'ProjectionExpression': projection_expression})

    if expr_attr_names:
        kwargs.update({'ExpressionAttributeNames': expr_attr_names})

    if index_name:
        kwargs.update({'IndexName': index_name})

    resp = table.query(**kwargs)
    data = resp['Items']

    while 'LastEvaluatedKey' in resp:
        kwargs.update({'ExclusiveStartKey': resp['LastEvaluatedKey']})
        resp = table.query(**kwargs)
        data.extend(resp['Items'])

    return data


items = query_all_items(
    Key('partkey').eq(partkey),
    table=table,
    filter_expression=Attr(id_field).is_in(ids)
)
print(f'items={items}, items length = {items.__len__()}')
