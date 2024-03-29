from config.config import BASE_API_RESPONSE

class apiResponseServide:
    
    def success_response(self, result):
        return {
            "status": BASE_API_RESPONSE['REQUEST_SUCCESS'],
            "result": result
        }
        
    def bad_response(self, result):
        return {
            "status": BASE_API_RESPONSE['BAD_REQUEST'],
            "result": result
        }