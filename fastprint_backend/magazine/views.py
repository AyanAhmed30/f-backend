from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from decimal import Decimal

@api_view(['GET'])
def get_dropdowns(request):
    return Response({
        "trim_sizes": TrimSizeSerializer(TrimSize.objects.all(), many=True).data,
        "interior_colors": InteriorColorSerializer(InteriorColor.objects.all(), many=True).data,
        "paper_types": PaperTypeSerializer(PaperType.objects.all(), many=True).data,
        "cover_finishes": CoverFinishSerializer(CoverFinish.objects.all(), many=True).data,
        "binding_types": BindingTypeSerializer(BindingType.objects.all(), many=True).data,
    })

@api_view(['GET'])
def get_bindings(request):
    page_count = int(request.GET.get('page_count', 0))
    if page_count >= 32:
        bindings = BindingType.objects.all()
    elif page_count >= 24:
        bindings = BindingType.objects.filter(name__in=['Coil Bound', 'Saddle Stitch', 'Case Wrap'])
    elif page_count >= 4:
        bindings = BindingType.objects.filter(name__in=['Coil Bound', 'Saddle Stitch'])
    elif page_count >= 3:
        bindings = BindingType.objects.filter(name='Coil Bound')
    else:
        bindings = BindingType.objects.none()
    return Response(BindingTypeSerializer(bindings, many=True).data)

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    try:
        pages = int(data['page_count'])
        qty = int(data['quantity'])

        binding = BindingType.objects.get(id=data['binding_id'])
        interior = InteriorColor.objects.get(id=data['interior_color_id'])
        paper = PaperType.objects.get(id=data['paper_type_id'])
        cover = CoverFinish.objects.get(id=data['cover_finish_id'])

        binding_price = binding.price
        interior_price = interior.price_per_page * pages
        paper_price = paper.price_per_page * pages
        cover_price = cover.price

        cost_per_book = binding_price + interior_price + paper_price + cover_price
        total_cost = cost_per_book * qty

        if qty > 100:
            discount = total_cost * Decimal('0.05')
            total_cost -= discount

        return Response({
            "cost_per_book": round(cost_per_book, 2),
            "total_cost": round(total_cost, 2)
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)

def update_price(type_name):
    model_map = {
        'interior': (InteriorColor, 'price_per_page'),
        'paper': (PaperType, 'price_per_page'),
        'cover': (CoverFinish, 'price'),
        'binding': (BindingType, 'price'),
    }

    def view_func(request, pk):
        Model, field = model_map[type_name]
        try:
            instance = Model.objects.get(pk=pk)
            new_price = request.data.get(field)
            setattr(instance, field, new_price)
            instance.save()
            return Response({field: getattr(instance, field)})
        except Model.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return api_view(['PUT'])(view_func)
