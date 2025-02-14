from rest_framework.serializers import ModelSerializer

from finance.models import Category


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        extra_kwargs = {
            'image': {'required': False}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = 200
        return data