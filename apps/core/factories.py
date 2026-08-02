import factory

#Abstract factory class for use in all Django models
class BaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True