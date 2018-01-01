import boto3
import json

s3 = boto3.client('s3')
athena = boto3.client('athena')

def lambda_handler(event, context):
    database_name = 'cerner'
    output_location = 's3://cerner-shipit/user-query-execution-output/'
    
    waiter = s3.get_waiter('object_exists')
    
    waiter.wait(Bucket='cerner-shipit', Key='conf/settings.txt')
    
    get_response = s3.get_object(
        Bucket='cerner-shipit',
        Key='conf/settings.txt'
        )
    body = get_response['Body'].read().decode('utf-8')
    
    files = body.split(' ')
    
    get_response = s3.get_object(
        Bucket=event['Records'][0]['s3']['bucket']['name'], 
        Key=files[2]
        )
        
    body = get_response['Body'].read().decode('utf-8')
    
    print(body)
    query = body.strip()
    print(query)
    
    execution_response = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': output_location,
            'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
            }
        }
    )
    
    execution_id = execution_response['QueryExecutionId']
    manifest = {
                    "fileLocations": [
                        {
                            "URIs": [
                                output_location + execution_id + '.csv'
                            ]
                        }
                    ],
                    "globalUploadSettings": {
                        "format": "CSV",
                        "delimiter": ",",
                        "textqualifier": "'",
                        "containsHeader": "true"
                    }
               }
    print(manifest)
    
    s3.put_object(
        Bucket='cerner-shipit',
        Key='conf/manifest.json',
        Body=json.dumps(manifest)
    )
    return
