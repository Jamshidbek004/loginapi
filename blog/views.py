from rest_framework.decorators import api_view
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from functools import reduce
import operator
from rest_framework import status
from blog.serializer import *
from .models import Tavar
from rest_framework import viewsets
from rest_framework.response import Response



class TavarViewSet(viewsets.ModelViewSet):
    serializer_class = TavarSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nomi = serializer.validated_data['nom']
        if not Tavar.objects.filter(nom=nomi).exists():
            self.perform_create(serializer)
            return Response({"message": "Saqlandi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Bu tavar allaqachon qo'shilgan boshqa tavar qo'shing yoki shu tavarni yangilang"}, status=status.HTTP_400_BAD_REQUEST)


class TavarnomViewSet(viewsets.ModelViewSet):
    queryset = Tavar_nomi.objects.all()
    serializer_class = TavarnomSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nomi = serializer.validated_data['nom']
        if not Tavar_nomi.objects.filter(nom=nomi).exists():
            self.perform_create(serializer)
            return Response({"message": "Saqlandi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Bu tavar allaqachon qo'shilgan"}, status=status.HTTP_400_BAD_REQUEST)

class TavarViewSet(viewsets.ModelViewSet):
    queryset = Tavar.objects.all()
    serializer_class = TavarSerializer

class MijozTavarViewSet(viewsets.ModelViewSet):
    queryset = MijozTavar.objects.all()
    serializer_class = MijozTavarSerializer

class TavarRasmiylashtirishViewSet(viewsets.ModelViewSet):
    queryset = Tavar_rasmiylashtirish.objects.all()
    serializer_class = TavarRasmiylashtirishSerializer

class SavatDeleteAPIView(DestroyAPIView):
    queryset = MijozTavar.objects.all()
    serializer_class = MijozTavarSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Maxsulot savatchadan o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def buyurtmalarim(request):
    m = Tavar_rasmiylashtirish.objects.filter(mijoz=request.user)
    serializer = TavarRasmiylashtirishSerializer(m, many=True)
    return Response(serializer.data)

class TavarRasmiylashtirishViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Tavar_rasmiylashtirish.objects.all()
        tavar = get_object_or_404(queryset, pk=pk)
        serializer = TavarRasmiylashtirishSerializer(tavar)
        return Response(serializer.data)

    def create_comment(self, request, tavar_id):
        tavar = get_object_or_404(Tavar_rasmiylashtirish, id=tavar_id)
        comments = tavar.comments.all()
        comment_count = comments.count()
        new_comment = None

        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                new_comment = serializer.save(products=tavar.mahsulot, user=request.user)
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer()
        tavar_serializer = TavarRasmiylashtirishSerializer(tavar)

        return Response({
            'tavar': tavar_serializer.data,
            'comments': CommentSerializer(comments, many=True).data,
            'new_comment': CommentSerializer(new_comment).data if new_comment else None,
            'comment_form': serializer.data,
            'comment_count': comment_count
        }, status=status.HTTP_200_OK)


class TavarSearchAPIView(APIView):
    def get(self, request):
        text = request.GET.get('query', None)
        queryset = Tavar.objects.all()

        if text:
            text_ajratish = text.split(' ')
            query = reduce(operator.and_, (Q(nom__icontains=i) | Q(iSHCH_mamlakat__icontains=i) for i in text_ajratish))
            queryset = queryset.filter(query)

        serializer = TavarSerializer(queryset, many=True)

        # Oxshash tavarlar
        oxshash_tavarlar = Tavar.objects.none()
        if queryset.exists():
            asosiy_tavarlar_id = queryset.values_list('id', flat=True)
            oxshash_tavarlar = Tavar.objects.filter(
                Q(narxi__in=queryset.values_list('narxi', flat=True)) |
                Q(iSHCH_mamlakat__in=queryset.values_list('iSHCH_mamlakat', flat=True))
            ).exclude(id__in=asosiy_tavarlar_id)

        oxshash_serializer = TavarSerializer(oxshash_tavarlar, many=True)

        return Response({'asosiy_tavarlar': serializer.data, 'oxshash_tavarlar': oxshash_serializer.data})

@api_view(['GET'])
def kassa(request):
    tavar_rasmiylashtirishlar = Tavar_rasmiylashtirish.objects.all()
    serializer = TavarRasmiylashtirishSerializer(tavar_rasmiylashtirishlar, many=True)
    return Response(serializer.data)


class KassaDetelAPIView(APIView):
    def post(self, request, id):
        tavar = get_object_or_404(Tavar_rasmiylashtirish, id=id)
        kassa_serializer = KassaSerializer(data=request.data)

        if kassa_serializer.is_valid():
            kod = kassa_serializer.validated_data['kod']
            if tavar.kod == kod:
                kassa = Kassa(kod=kod, yuk=tavar)
                kassa.save()
                return Response({'message': 'Kassa saved successfully'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Kod mos kelmadi.'}, status=status.HTTP_400_BAD_REQUEST)


class SearchResultList2APIView(APIView):
    def get(self, request):
        queryset = Tavar_rasmiylashtirish.objects.all()  # Adjust this queryset as needed
        text = self.request.GET.get('query', None)

        if text:
            text_ajratish = text.split(' ')
            text_ol = reduce(operator.and_,
                             (Q(kod__icontains=i) for i in text_ajratish)
                             )
            queryset = queryset.filter(text_ol)

        serializer = TavarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)