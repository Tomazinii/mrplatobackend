# from random import randint
# from rest_framework.test import APIClient
# from faker import Faker
# import pytest

# faker = Faker()


# pytestmark = pytest.mark.endpoint

# class TestEndpointGroup:
    
#     endpoint = '/api/v1/groups/'

#     def test_create_group(self, api_client):

#         body = {
#             "name": faker.name(),
#             "turma": randint(0,50)
#         }

#         response = api_client().post(
#             self.endpoint,
#             body,
#         )

#         assert response.status_code == 201
        