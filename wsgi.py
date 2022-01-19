from urls import routes
from framework.front_controllers import other_front, secret_front
from framework.application import Application


fronts = [secret_front, other_front]

app_object = Application(routes, fronts)
