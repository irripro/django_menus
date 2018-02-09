from django.apps import AppConfig


class DjangoMenusConfig(AppConfig):
    name = 'django_menus'
    #def ready(self):
    #    pass
    def ready(self):
        #? possibly look for circular dependencies, and resolve some URL stuff?
        #https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
        print('...........menu ready()')
