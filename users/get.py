from lib.users import Users
from lib.utils import response_builder, logger
from botocore.exceptions import ClientError
users = Users()


def get(event, context):
    try:
        logger.info(event)
        user_id = event['pathParameters']['user_id']

        if not users.exists_user(user_id=user_id):
            return response_builder(404, {
                'error_message': 'そのユーザは存在しません'
            })

        result = users.get(user_id=user_id)

    except ClientError as e:
        logger.error(e)
        return response_builder(500, {
            'error_message': 'Internal Server Error'
        })

    return response_builder(200, result['Item'])
