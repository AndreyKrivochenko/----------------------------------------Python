from framework.front_controllers import OtherFront, SecretFront
from urls import routes
from framework.application import Application


fronts = [SecretFront(), OtherFront()]

app_object = Application(routes, fronts)
