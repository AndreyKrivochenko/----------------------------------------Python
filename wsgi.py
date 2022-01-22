from framework import OtherFront, SecretFront, Application
from urls import routes


fronts = [SecretFront(), OtherFront()]

app_object = Application(routes, fronts)
