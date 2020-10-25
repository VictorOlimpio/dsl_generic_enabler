from djongo import models

class Model(models.Model):
    modelName = models.CharField(max_length=100)
    windowSize = models.CharField(max_length=10)
    preTrainSize = models.CharField(max_length=10)
    nSamples = models.CharField(max_length=10)
    # model = models.FieldFile()
    class Meta:
        abstract = True

class Subscription(models.Model):
    url = models.CharField(max_length=100)

    class Meta:
        abstract = True
class EntityModel(models.Model):
    entity_id = models.CharField(max_length=100, primary_key=True, unique=True)
    entity_type = models.CharField(max_length=100)
    model = models.EmbeddedField(model_container=Model, default=None)
    Subscription = models.EmbeddedField(model_container=Subscription, default=None)

