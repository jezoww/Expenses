from rest_framework.serializers import ModelSerializer

from finance.models import Category, Expense


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name', 'image'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = 200
        return data


class ExpenseModelSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

        extra_kwargs = {
            'user': {'read_only': True, 'required': False}
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data

        data['status'] = 200
        return data


class HistoryModelSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategoryModelSerializer(
            instance=Category.objects.filter(id=data.get('category')).first()).data
        data['status'] = 200
        return data


class ExpenseDeleteModelSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = 'id', 'money', 'description'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = 200
        return data