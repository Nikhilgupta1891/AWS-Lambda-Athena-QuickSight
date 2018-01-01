import boto3

s3 = boto3.client('s3')
athena = boto3.client('athena')

def lambda_handler(event, context):
    database_name = 'cerner'
    output_location = 's3://cerner-shipit/create-table-execution-output/'
    get_response = s3.get_object(
        Bucket=event['Records'][0]['s3']['bucket']['name'], 
        Key=event['Records'][0]['s3']['object']['key']
        )
    body = get_response['Body'].read().decode('utf-8')
    
    lines = body.split('\n')
    table_name = lines[0].strip()
    print(table_name)
    
    schema = lines[1].strip()
    print(schema)
    
    create_table_query = ('CREATE EXTERNAL TABLE IF NOT EXISTS ' 
                      + database_name 
                      + '.' + table_name 
                      + '(' + schema + ')'
                      + ' ROW FORMAT SERDE \'org.apache.hadoop.hive.serde2.OpenCSVSerde\''
                      + ' LOCATION \'' + 's3://cerner-shipit/data' + '\'')
    
    print(create_table_query)
    
    waiter = s3.get_waiter('object_exists')
    
    waiter.wait(Bucket='cerner-shipit', Key='conf/settings.txt')
    
    get_response = s3.get_object(
        Bucket='cerner-shipit',
        Key='conf/settings.txt'
        )
    body = get_response['Body'].read().decode('utf-8')
    
    files = body.split(' ')
    
    waiter = s3.get_waiter('object_exists')
    
    waiter.wait(Bucket='cerner-shipit', Key=files[0])
    
    athena.start_query_execution(
        QueryString=create_table_query,
        ResultConfiguration={
            'OutputLocation': output_location,
            'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
            }
        }
    )
    return
