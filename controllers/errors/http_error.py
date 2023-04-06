
class HttpErrors:
    """ class defin erros """

    @staticmethod
    def error_422():
        return {"status_code": 422, "body":"Unprocessable entity"}

    @staticmethod
    def error_400():
        return {"status_code": 400, "body":{"error":"Bad Request"}}