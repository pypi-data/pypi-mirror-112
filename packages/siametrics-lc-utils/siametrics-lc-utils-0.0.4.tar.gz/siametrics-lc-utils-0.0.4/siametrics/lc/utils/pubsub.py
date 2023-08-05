import boto3
import json

from .settings import settings


client = boto3.client(
    'sns',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_SNS_KEY,
    aws_secret_access_key=settings.AWS_SNS_SECRET,
)


def publish(topic, body=None, path=None, json_encoder=None) -> None:
    message = {
        'body': body,
        'path': path,
    }

    # if settings.PRODUCTION:
    #     segment = xray_recorder.current_segment()
    #     message['trace_id'] = segment.trace_id

    message = json.dumps(message, cls=json_encoder)
    message = json.dumps({"default": message})
    resp = client.publish(
        TopicArn=f'{settings.AWS_SNS_PATH}{settings.ENVIRONMENT}-{topic}',
        Message=message,
        MessageStructure="json",
    )
    print('SNS response:', resp)
