
from infra.user.models import RegisterStudents
import json


def create_list_email():
    object = RegisterStudents.objects.last()
    if object:
        archive = object.archive.open()
        data = json.load(archive)

        list_email = []
        for z in data["dict"]:
            list_email.append(z["email"])

        return list_email

    return None
