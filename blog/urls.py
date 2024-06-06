from django.urls import path
from blog.views import *

urlpatterns = [
    path('tavar/', TavarViewSet.as_view({'post': 'create'}), name='tavar-create'),
    path('tavarnom/', TavarnomViewSet.as_view({'post': 'create'}), name='tavarnom-create'),
    path('mijoztavar/', MijozTavarViewSet.as_view({'get': 'list'}), name='mijoztavar-list'),
    path('tavarrasmiylashtirish/', TavarRasmiylashtirishViewSet.as_view({'get': 'list'}),
         name='tavarrasmiylashtirish-list'),
    path('savat/<int:pk>/delete/', SavatDeleteAPIView.as_view(), name='savat-delete'),
    path('buyurtmalarim/', buyurtmalarim, name='buyurtmalarim'),
    path('tavarrasmiylashtirish/<int:pk>/', TavarRasmiylashtirishViewSet.as_view({'get': 'retrieve'}),
         name='tavarrasmiylashtirish-detail'),
    path('tavarrasmiylashtirish/<int:tavar_id>/create_comment/',
         TavarRasmiylashtirishViewSet.as_view({'post': 'create_comment'}), name='tavarrasmiylashtirish-create-comment'),
    path('tavarsearch/', TavarSearchAPIView.as_view(), name='tavarsearch'),
    path('kassa/', kassa, name='kassa'),
    path('kassa/<int:id>/detel/', KassaDetelAPIView.as_view(), name='kassa-detel'),
    path('searchresult2/', SearchResultList2APIView.as_view(), name='searchresult2'),
]