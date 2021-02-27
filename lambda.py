import json
import boto3
import datetime

def lambda_handler(event, context):
    string = "Hello Lambda"
    encoded_string = string.encode("utf-8")
    bucket_name = "mys3bucket-test"
    file_name = 'my_file.txt'
    s3_path = "/" + str(datetime.datetime.now()) + "/" + file_name


    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
    return {
        'statusCode': 200,
        'body': json.dumps('file is created in:'+s3_path)
    }
