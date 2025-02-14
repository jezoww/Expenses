from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from finance.choices import ExpenseTypeChoice
from finance.models import Expense, Category
from finance.permissions import ExpenseOwnedPermission
from finance.serializers import CategoryModelSerializer, ExpenseModelSerializer, ExpenseDeleteModelSerializer


@extend_schema(tags=['category'], responses=CategoryModelSerializer, parameters=[
    OpenApiParameter(
        name="type",
        description="Order holati bo'yicha filtrlash uchun.",
        type={"type": "string"},
        enum=[choice[0] for choice in ExpenseTypeChoice.choices],
        required=True,
    )
])
class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryModelSerializer

    def get_queryset(self):
        return Category.objects.filter(type=self.request.query_params.get('type'))




@extend_schema(tags=['Expense'], responses=ExpenseModelSerializer)
class ExpenseCreateAPIView(CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseModelSerializer
    permission_classes = IsAuthenticated,

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=['Expense'], responses=ExpenseModelSerializer)
class ExpenseUpdateAPIView(UpdateAPIView):
    permission_classes = IsAuthenticated, ExpenseOwnedPermission,
    queryset = Expense.objects.all()
    serializer_class = ExpenseModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['Expense'])
@permission_classes([IsAuthenticated])
class ExpenseDestroyAPIView(APIView):
    def post(self, request, pk):
        kirim_chiqim = Expense.objects.filter(id=pk)
        if not kirim_chiqim or kirim_chiqim.first().user != request.user:
            return JsonResponse({"error": "Expenses not found!"}, status=HTTP_404_NOT_FOUND)
        serialized_data = ExpenseDeleteModelSerializer(instance=kirim_chiqim.first()).data
        kirim_chiqim.delete()
        return JsonResponse(serialized_data)

@extend_schema(tags=['Expense'])
@permission_classes([IsAuthenticated, ExpenseOwnedPermission])
class ExpenseRetrieveAPIView(RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Expense.objects.all()
    serializer_class = ExpenseModelSerializer



# @extend_schema(tags=['history'], parameters=[
#     OpenApiParameter(
#         name="period",
#         description="Order holati bo'yicha filtrlash uchun.",
#         type={"type": "string"},
#         enum=['today', 'week', 'month', 'year'],
#         required=False,
#     ),
#     OpenApiParameter(
#         name="status",
#         description="Order holati bo'yicha filtrlash uchun.",
#         type={"type": "string"},
#         enum=[choice[0] for choice in ExpenseStatusChoice.choices],
#         required=False,
#     ),
#
# ])
@extend_schema(tags=['Expense'])
@permission_classes([IsAuthenticated])
class ExpenseListAPIView(ListAPIView):
    serializer_class = ExpenseModelSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    # def get(self, request):
    #     period = request.GET.get('period', None)
    #     status = request.GET.get('status', None)
    #     history = Expense.objects.filter(user=request.user).order_by('-created_at')
    #     if status:
    #         if status == 'profit':
    #             history = history.filter(status=ExpenseStatusChoice.PROFIT)
    #         elif status == 'loss':
    #             history = history.filter(status=ExpenseStatusChoice.LOSS)
    #
    #     if period:
    #         if period == 'today':
    #             history = history.filter(created_at__gte=now() - timedelta(days=1))
    #         elif period == 'week':
    #             history = history.filter(created_at__gte=now() - timedelta(weeks=1))
    #         elif period == 'month':
    #             history = history.filter(created_at__gte=now() - timedelta(days=30))
    #         elif period == 'year':
    #             history = history.filter(created_at__gte=now() - timedelta(days=365))
    #
    #     income = 0
    #     expenses = 0
    #     category_id = request.data.get('category_id', None)
    #
    #     if category_id:
    #         history = history.filter(category_id=category_id)
    #
    #     for w in history:
    #         if w.status == ExpenseStatusChoice.PROFIT:
    #             income += w.money
    #         elif w.status == ExpenseStatusChoice.LOSS:
    #             expenses += w.money
    #
    #     data = {"history": HistoryModelSerializer(instance=history, many=True).data,
    #             'income': income,
    #             'expenses': expenses}
    #
    #     return JsonResponse(data)


# @extend_schema(tags=['total'], parameters=[
#     OpenApiParameter(
#         name="category_id",
#         description=(
#                 "..."
#         ),
#         type={
#             "type": "integer",
#         },
#         explode=False,
#         style="form",
#         required=False
#     )
# ])
@permission_classes([IsAuthenticated])
class TotalAPIView(APIView):
    def get(self, request):
        income = 0
        expenses = 0
        category_id = request.data.get('category_id', None)

        objs = Expense.objects.filter(user=request.user)

        if category_id:
            objs = objs.filter(category_id=category_id)

        for w in objs:
            if w.type == ExpenseTypeChoice.PROFIT:
                income += w.money
            elif w.type == ExpenseTypeChoice.LOSS:
                expenses += w.money

        return JsonResponse({'total': income - expenses, 'income': income, 'expenses': expenses})
