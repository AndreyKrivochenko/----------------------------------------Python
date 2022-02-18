from framework import OtherFront, SecretFront, Application
from pages import routes

fronts = [SecretFront(), OtherFront()]

app_object = Application(routes, fronts)
