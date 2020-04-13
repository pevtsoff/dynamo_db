import itertools
import boto3
from boto3.dynamodb.conditions import Key

# this helper allows to query all table items without limits
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("your_table_name")
partkey = "yourpartkey"


def query_all_items(table, **kwargs):
    while 'LastEvaluatedKey' in (resp := table.query(**kwargs)):
        kwargs.update({'ExclusiveStartKey': resp['LastEvaluatedKey']})
        resp = table.query(**kwargs)

        yield resp['Items']


items = list(itertools.chain(*query_all_items(
    KeyConditionExpression=Key('partkey').eq(partkey),
    table=table,
)))

print(f'items={items}, items length = {items.__len__()}')