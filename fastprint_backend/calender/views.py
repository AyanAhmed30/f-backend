from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from decimal import Decimal

@api_view(['GET'])
def get_dropdowns(request):
    return Response({
        "bindings": BindingTypeSerializer(BindingType.objects.all(), many=True).data,
        "interior_colors": InteriorColorSerializer(InteriorColor.objects.all(), many=True).data,
        "paper_types": PaperTypeSerializer(PaperType.objects.all(), many=True).data,
        "cover_finishes": CoverFinishSerializer(CoverFinish.objects.all(), many=True).data,
    })

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    try:
        qty = int(data['quantity'])
        binding = BindingType.objects.get(id=data['binding_id'])
        base_price = binding.price

        total_price = base_price * qty
        discount = total_price * Decimal(0.05) if qty > 100 else Decimal(0)
        final_amount = total_price - discount

        return Response({
            "cost_per_book": round(base_price, 2),
            "total_cost": round(total_price, 2),
            "discounted_amount": round(discount, 2),
            "amount_after_discount": round(final_amount, 2)
        })
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def get_bindings(request):
    trim_size_id = request.GET.get('trim_size_id')
    page_count = request.GET.get('page_count')

    try:
        # If either trim_size_id or page_count is missing, assume it's a general or calendar request
        if not trim_size_id or not page_count:
            bindings = BindingType.objects.all()
        else:
            # Apply filtering if needed
            bindings = BindingType.objects.all()
            # You can filter based on trim_size_id and page_count here if you want in the future

        serializer = BindingTypeSerializer(bindings, many=True)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
from rest_framework import status

@api_view(['PUT'])
def update_binding_type(request, pk):
    try:
        binding = BindingType.objects.get(pk=pk)
        serializer = BindingTypeSerializer(binding, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except BindingType.DoesNotExist:
        return Response({"error": "Binding type not found"}, status=404)


@api_view(['PUT'])
def update_interior_color(request, pk):
    try:
        color = InteriorColor.objects.get(pk=pk)
        serializer = InteriorColorSerializer(color, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except InteriorColor.DoesNotExist:
        return Response({"error": "Interior color not found"}, status=404)


@api_view(['PUT'])
def update_paper_type(request, pk):
    try:
        paper = PaperType.objects.get(pk=pk)
        serializer = PaperTypeSerializer(paper, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except PaperType.DoesNotExist:
        return Response({"error": "Paper type not found"}, status=404)


@api_view(['PUT'])
def update_cover_finish(request, pk):
    try:
        finish = CoverFinish.objects.get(pk=pk)
        serializer = CoverFinishSerializer(finish, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except CoverFinish.DoesNotExist:
        return Response({"error": "Cover finish not found"}, status=404)
