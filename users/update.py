import json
from lib.users import Users
from lib.utils import response_builder, logger
from botocore.exceptions import ClientError
users = Users()


def update(event, context):
    try:
        logger.info(event)
        data = json.loads(event['body'])
        user_id = event['pathParameters']['user_id']

        if 'email' not in data:
            return response_builder(400, {
                'error_message': 'emailのパラメータが足りません'
            })

        if not users.exists_user(user_id=user_id):
            return response_builder(400, {
                'error_message': '既にそのユーザは存在していません'
            })

        users.update(
            user_id=user_id,
            email=data['email'],
        )
    except json.decoder.JSONDecodeError:
        return response_builder(400, {
            'error_message': 'JSONが不正です'
        })

    except ClientError as e:
        logger.error(e)
        return response_builder(500, {
            'error_message': 'Internal Server Error'
        })

    return response_builder(204)
