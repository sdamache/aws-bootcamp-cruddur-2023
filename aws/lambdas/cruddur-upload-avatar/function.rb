require 'aws-sdk-s3'
require 'json'
require 'jwt'

def handler(event:,context:)
    puts event
    # returns cors headers for pre-flight check
    if event['routeKey'] == 'OPTIONS /{proxy+}'
        puts({step: "pre-flight", message: "pre flight CORS check"}.to_json)
        {
            headers: {
            "Access-Control-Allow-Headers": "*, Authorization",
            "Access-Control-Allow-Origin": "https://3000-sdamache-awsbootcampcru-0ihiu33o0d7.ws-us100.gitpod.io",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
        statusCode: 200
    }
    else
        token = event['headers']['authorization'].split(' ')[1]
        puts({step: 'pre-signed url', access_token: token}.to_json)

        body_hash = JSON.parse(event['body'])
        extension = body_hash['extension']
        puts({step: 'pre-signed url', extension: extension, body_hash: body_hash}.to_json)

        decoded_token = JWT.decode token, nil, false
        cognito_username = decoded_token[0]['sub']
        s3 = Aws::S3::Resource.new
        bucket_name = ENV['UPLOADS_BUCKET_NAME']
        object_key = "#{cognito_username}.#{extension}"

        puts({step: 'object upload', bucket_name: bucket_name, object_key: object_key}.to_json)

        obj = s3.bucket(bucket_name).object(object_key)
        url = obj.presigned_url(:put, expires_in: 60 * 5)
        url #this is the data that will be returned
        body = {url: url}.to_json
        {
            headers: {
            "Access-Control-Allow-Headers": "*, Authorization",
            "Access-Control-Allow-Origin": "https://3000-sdamache-awsbootcampcru-0ihiu33o0d7.ws-us100.gitpod.io",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
        statusCode: 200,
        body: body
        }
    end #if
end #handler