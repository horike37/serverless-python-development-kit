import boto3
import os
import time
dynamodb = boto3.resource('dynamodb')


class Users():
    def __init__(self):
        self.users_table = dynamodb.Table(os.environ['DYNAMODB_TABLE_USERS'])

    def create(self, user_id, email):
        timestamp = int(time.time() * 1000)
        item = {
            'user_id': user_id,
            'email': email,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }

        self.users_table.put_item(Item=item)

    def update(self, user_id, email):
        timestamp = int(time.time() * 1000)
        self.users_table.update_item(
            Key={
                'user_id': user_id
            },
            ExpressionAttributeNames={
              '#user_email': 'email',
            },
            ExpressionAttributeValues={
              ':email': email,
              ':updatedAt': timestamp,
            },
            UpdateExpression='SET #user_email = :email, '
                             'updatedAt = :updatedAt',
            ReturnValues='ALL_NEW',
        )

    def get(self, user_id):
        return self.users_table.get_item(
            Key={
                'user_id': user_id
            }
        )

    def get_all(self):
        return self.users_table.scan()

    def delete(self, user_id):
        self.users_table.delete_item(
            Key={
                'user_id': user_id
            }
        )

    def exists_user(self, user_id):
        result = self.users_table.get_item(
            Key={
                'user_id': user_id
            }
        )

        return 'Item' in result
