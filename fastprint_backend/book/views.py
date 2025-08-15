from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import BookProject
from .serializers import BookProjectSerializer

import logging

logger = logging.getLogger(__name__)


class UploadBookProjectView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def post(self, request):
        data = request.data.copy()
        cover_file = request.FILES.get('cover_file')
        cover_description = data.get('cover_description')

        # Must provide either a cover file or a cover description
        if not cover_file and not cover_description:
            return Response({
                'status': 'error',
                'message': 'Please provide either a cover file or a cover description.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookProjectSerializer(data=data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({
                    'status': 'success',
                    'message': 'Book project uploaded successfully.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error("Error saving BookProject", exc_info=True)
                return Response({
                    'status': 'error',
                    'message': 'An error occurred while saving the project.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning("Validation error: %s", serializer.errors)
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_books(request):
    """
    Return all books uploaded by the current authenticated user.
    """
    try:
        books = BookProject.objects.filter(user=request.user).order_by('-created_at')
        serializer = BookProjectSerializer(books, many=True)
        return Response({
            'status': 'success',
            'results': len(serializer.data),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error("Failed to fetch user's book projects", exc_info=True)
        return Response({
            'status': 'error',
            'message': 'Failed to fetch your book projects.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    """
    Retrieve a single book project by ID for the authenticated user.
    """
    try:
        book = BookProject.objects.get(pk=pk, user=request.user)
    except BookProject.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Book project not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = BookProjectSerializer(book)
    return Response({
        'status': 'success',
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_book(request, pk):
    """
    Update an existing book project by ID for the authenticated user.
    """
    try:
        book = BookProject.objects.get(pk=pk, user=request.user)
    except BookProject.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Book project not found.'
        }, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = BookProjectSerializer(book, data=request.data, partial=partial)

    # Validate presence of cover_file or cover_description if both are missing in update
    cover_file = request.FILES.get('cover_file')
    cover_description = request.data.get('cover_description') or book.cover_description

    if not cover_file and not cover_description:
        return Response({
            'status': 'error',
            'message': 'Please provide either a cover file or a cover description.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        try:
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Book project updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error updating BookProject", exc_info=True)
            return Response({
                'status': 'error',
                'message': 'An error occurred while updating the project.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        logger.warning("Validation error on update: %s", serializer.errors)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request, pk):
    """
    Delete a book project by ID for the authenticated user.
    """
    try:
        book = BookProject.objects.get(pk=pk, user=request.user)
        book.delete()
        return Response({
            'status': 'success',
            'message': 'Book project deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)
    except BookProject.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Book project not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error("Error deleting BookProject", exc_info=True)
        return Response({
            'status': 'error',
            'message': 'An error occurred while deleting the project.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_all_orders(request):
    if not request.user.is_staff:
        return Response({"detail": "Not authorized."}, status=403)

    orders = BookProject.objects.all().order_by("-created_at")
    data = []
    for order in orders:
        data.append({
            "id": order.id,
            "title": order.title,
            "user_email": order.user.email,
            "category": order.category,
            "language": order.language,
            "page_count": order.page_count,
            "created_at": order.created_at,
            "binding_type": order.binding_type,
            "cover_finish": order.cover_finish,
            "interior_color": order.interior_color,
            "paper_type": order.paper_type,
            "trim_size": order.trim_size,
            "pdf_file": order.pdf_file.url if order.pdf_file else None,
            "cover_file": order.cover_file.url if order.cover_file else None,
            "cover_description": order.cover_description,
            
            
        })

    return Response({
        "status": "success",
        "results": len(data),
        "data": data
    })
