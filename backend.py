import boto3
from pprint import pprint
dynamodb = boto3.client('dynamodb')
import json


# Operaciones CRUD

def create_item(item):
 
    response = dynamodb.put_item(TableName= "note-table" , Item=item)
    return response


def read_item(tablename):
   
    response  = dynamodb.scan(TableName=tablename)


def delete_item(item_id):
   
    response = dynamodb.delete_item(
        TableName='note-table',
        Key={'id': {'N': item_id }}
    )
    return response


def update_item(item_id,update_expression,expression_attribute_values):
   
    response = dynamodb.update_item(
        TableName='note-table',
        Key={'id': {'N': item_id }},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )
    return response


import json
def lambda_handler(event, context):

    http_method = event['httpMethod']
    if http_method == 'POST':
        new_item = {
            'id': {"N": "2"},
            'descripcion': {"S": "david"}, 
            }
        create_item(new_item)
    elif http_method == 'GET':
        pprint(read_item("note-table")["Items"]) 
        message = 'Se realiza una petición de tipo GET'
    elif http_method == 'DELETE':
        delete_item('2')
        message = 'Se realiza una petición de tipo DELETE'
    elif http_method == 'PUT':
        update_item('2','SET descripcion = :new_desc',{':new_desc': {'S': 'pedro'}})
        message = 'Se realiza una petición de tipo PUT'
    else:
        message = 'Tipo de petición no soportada'
    
    return {
    'statusCode': 200,
    'body': json.dumps(message)
  }
