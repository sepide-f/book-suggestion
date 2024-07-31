from rest_framework.views import APIView
from .models import Books, Review
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.db import connection
from rest_framework.permissions import IsAuthenticated


class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT
                            b.title,
                            b.author,
                            b.genre,
                            b.id,
                            r.book_id,
                            r.rating
                    FROM
                            boks_books b
                    LEFT JOIN boks_review r on b.id = r.book_id
                    WHERE
                            r.user_id = %s
                """
                cursor.execute(query,[user])
                rows = cursor.fetchall()
                return JsonResponse(rows, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookListByGenre(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, genre):
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT 
                    *
                FROM 
                    boks_books b
                WHERE
                    b.genre = %s
                
                """
                cursor.execute(query, [genre])
                rows = cursor.fetchall()
                return JsonResponse(rows, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Review(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book = request.data.get('book')
        rating = request.data.get('rating')
        user = request.user.id

        try:
            with connection.cursor() as cursor:
                query = """
                        INSERT INTO boks_review (user_id, rating, book_id)
                        VALUES(%s, %s, %s)
                        """
                cursor.execute(query, [user, rating, book])
                return Response({'user_id': user, 'book_id': book, 'rating': rating},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        book = request.data.get('book')
        user = request.user.id
        rating = request.data.get('rating')
        try:
            with connection.cursor() as cursor:
                query = """
                        UPDATE boks_review
                        SET RATING = %s
                        WHERE 
                        user_id = %s and book_id =%s
                        """
                cursor.execute(query, [rating, user, book])
                return Response({'user_id': user, 'book_id': book, 'rating': rating},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        book = request.data.get('book')
        user = request.user.id
        try:
            with connection.cursor() as cursor:
                query = """
                       DELETE FROM boks_review
                        WHERE 
                        user_id = %s and book_id =%s
                        """
                cursor.execute(query, [user, book])
                return Response({'user_id': user, 'book_id': book},
                                status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
