from rest_framework.serializers import ModelSerializer

from finance.models import Category, KirimChiqim


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name',


class KirimChiqimModelSerializer(ModelSerializer):
    class Meta:
        model = KirimChiqim
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True, 'required': False}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data
        return data


class HistoryModelSerializer(ModelSerializer):
    class Meta:
        model = KirimChiqim
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data
        return data


class KirimChiqimDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = KirimChiqim
        fields = 'id', 'money', 'description'