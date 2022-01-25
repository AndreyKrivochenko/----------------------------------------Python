from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


# def render(template_name, **kwargs):
#
#     with open(template_name, encoding='utf-8') as f:
#         template = Template(f.read())
#
#     return template.render(**kwargs)

def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
