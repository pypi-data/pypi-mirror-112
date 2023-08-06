from . import gv
from django.template.loader import get_template


class BaseBodyTemplate:
    def __init__(self, request, context={}, *args, **kwargs):
        super(BaseBodyTemplate, self).__init__(*args, **kwargs)

        self.__context = context
        self.__request = request
        self.__template_body = ""

        self.generate_template()

    def generate_template(self):
        self.__context['menus'] = gv.menu_map

        self.__template_body = get_template('onepage/base.html').render(
            self.__context, request=self.__request
        )

    def as_text(self):
        return """{}""".format(self.__template_body)

    def as_html(self):
        return self.__template_body


class BaseNavTemplate:
    def __init__(self, request, context={}, *args, **kwargs):
        super(BaseNavTemplate, self).__init__(*args, **kwargs)

        self.__context = context
        self.__request = request
        self.__template_body = ""

    def generate_template(self):
        self.__context['menus'] = gv.menu_map

        self.__template_body = get_template('onepage/nav.html').render(
            self.__context, request=self.__request
        )

    def as_text(self):
        return """{}""".format(self.template_body)

    def as_html(self):
        return self.template_body
