from lambdas.http.users.create import handler
from unittest import mock
from botocore.exceptions import ClientError
import json


class TestUsersCreate(object):

    def test_without_email(self):
        event = {
            'body': '{"mail":"aaa"}',
            'pathParameters': {
                'user_id': 'xxxxx'
            }
        }

        result = handler(event, '')
        body = json.loads(result['body'])
        assert result['statusCode'] == 400
        assert body['error_message'] == 'emailのパラメータが足りません'

    @mock.patch('lambdas.http.users.create.users.exists_user')
    def test_duplicate_user(self, mock):
        mock.return_value = True
        event = {
            'body': '{"email":"aaa@example.com"}',
            'pathParameters': {
                'user_id': 'xxxxx'
            }
        }

        result = handler(event, '')
        body = json.loads(result['body'])
        assert result['statusCode'] == 409
        assert body['error_message'] == '既にそのユーザは存在しています'

    def test_invalid_json(self):
        event = {
            'body': '"mail":"aaa"}',
            'pathParameters': {
                'user_id': 'xxxxx'
            }
        }

        result = handler(event, '')
        body = json.loads(result['body'])
        assert result['statusCode'] == 400
        assert body['error_message'] == 'JSONが不正です'

    @mock.patch('lambdas.http.users.create.users.exists_user', side_effect=ClientError(
        {'error': 'error'}, 'error')
    )
    def test_500_error(self, mock):
        mock.return_value = True
        event = {
            'body': '{"email":"aaa@example.com"}',
            'pathParameters': {
                'user_id': 'xxxxx'
            }
        }

        result = handler(event, '')
        assert result['statusCode'] == 500
