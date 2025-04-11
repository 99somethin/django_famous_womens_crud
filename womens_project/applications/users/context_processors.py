from ..women import utils

def get_women_context(request):
    return {'mainmenu': utils.DataMixin.menu}