from dsl_broker.models import EntityModel

class EntityModelCreator:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def save(self):
        try:
            entity = self._create_instance()
            entity.save()
        except Exception as error:
            self.errors.append(error)

    def _create_instance(self):
        model_value = self.data['model']['value']
        entity = EntityModel()
        entity.entity_id = self.data['id']
        entity.entity_type = self.data['type']
        entity.model = model_value
        return entity