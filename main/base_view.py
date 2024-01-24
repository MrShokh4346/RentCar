from flask_apispec import MethodResource 

class BaseView(MethodResource):
    @classmethod
    def register(cls, blueprint, spec, url ,name):
        blueprint.add_url_rule(url, view_func=cls.as_view(name))
        blueprint.register_error_handler(422, cls.handler_error)
        spec.register(cls, blueprint=blueprint.name)
        
    @staticmethod
    def handler_error(err):
        header = err.data.get('handler', None)
        messages = err.data.get('messages', ['Invalid input'])
        if header:
            return {"meaasges":messages}, 400, header
        else:
            return {"meaasges":messages}, 400

         