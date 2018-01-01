def lambda_handler(event, context):
    InputLocation=''
    OutputLocation=''
    databaseName=''
    
    query=('')                
    client.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': OutputLocation,
            'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
            }
        }
    )
    
    return
