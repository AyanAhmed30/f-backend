from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from decimal import Decimal

@api_view(['GET'])
def get_dropdowns(request):
    return Response({
        "trim_sizes": TrimSizeSerializer(TrimSize.objects.all(), many=True).data,
        "bindings": BindingTypeSerializer(BindingType.objects.all(), many=True).data,
        "interior_colors": InteriorColorSerializer(InteriorColor.objects.all(), many=True).data,
        "paper_types": PaperTypeSerializer(PaperType.objects.all(), many=True).data,
        "cover_finishes": CoverFinishSerializer(CoverFinish.objects.all(), many=True).data,
    })

@api_view(['GET'])
def get_valid_bindings(request):
    try:
        page_count = int(request.GET.get('page_count', 0))
    except (ValueError, TypeError):
        return Response({"error": "Invalid or missing page count"}, status=400)

    all_bindings = BindingType.objects.all()
    valid_bindings = []

    for binding in all_bindings:
        name = binding.name.lower()
        if page_count >= 3 and "coil" in name:
            valid_bindings.append(binding)
        elif page_count >= 4 and ("coil" in name or "saddle" in name):
            valid_bindings.append(binding)
        elif page_count >= 24 and ("coil" in name or "saddle" in name or "case" in name):
            valid_bindings.append(binding)
        elif page_count >= 32 and (
            "perfect" in name or "coil" in name or "saddle" in name or "case" in name or "linen" in name
        ):
            valid_bindings.append(binding)

    serializer = BindingTypeSerializer(valid_bindings, many=True)
    return Response(serializer.data)

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

        base_price = binding.price
        interior_price = interior.price_per_page * pages
        paper_price = paper.price_per_page * pages
        cover_price = cover.price

        book_price = base_price + interior_price + paper_price + cover_price
        total_price = book_price * qty

        # Apply discount
        if qty > 100:
            discount = total_price * Decimal(0.05)
        else:
            discount = Decimal(0)

        final_amount = total_price - discount

        return Response({
            "cost_per_book": round(book_price, 2),
            "total_cost": round(total_price, 2),
            "discounted_amount": round(discount, 2),
            "amount_after_discount": round(final_amount, 2)
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)
@api_view(['PUT'])
def update_interior_color(request, pk):
    try:
        color = InteriorColor.objects.get(pk=pk)
        color.price_per_page = request.data['price_per_page']
        color.save()
        return Response({'success': 'Updated successfully'})
    except InteriorColor.DoesNotExist:
        return Response({'error': 'Interior color not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_paper_type(request, pk):
    try:
        paper = PaperType.objects.get(pk=pk)
        paper.price_per_page = request.data['price_per_page']
        paper.save()
        return Response({'success': 'Updated successfully'})
    except PaperType.DoesNotExist:
        return Response({'error': 'Paper type not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_cover_finish(request, pk):
    try:
        finish = CoverFinish.objects.get(pk=pk)
        finish.price = request.data['price']
        finish.save()
        return Response({'success': 'Updated successfully'})
    except CoverFinish.DoesNotExist:
        return Response({'error': 'Cover finish not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['PUT'])
def update_binding_type(request, pk):
    try:
        binding = BindingType.objects.get(pk=pk)
        binding.price = request.data['price']
        binding.save()
        return Response({'success': 'Updated successfully'})
    except BindingType.DoesNotExist:
        return Response({'error': 'Binding type not found'}, status=404)
    