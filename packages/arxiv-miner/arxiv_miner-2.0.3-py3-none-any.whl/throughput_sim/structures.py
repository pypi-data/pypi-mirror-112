import json
class Status:
    def __init__(self,\
                success_bool = False,
                wait_time = None,
                message=None
                ):
        self.success_bool = success_bool        
        self.wait_time = wait_time

    @property
    def json_string(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '''
        Success : {success_bool}
        wait_time  {wait_time}
        message= {message}
        '''.format(
            success_bool = self.success_bool,
            wait_time = str(self.wait_time),
            message = str(self.message),
        )