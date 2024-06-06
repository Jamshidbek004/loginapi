from rest_framework import serializers
from blog.models import Tavar, Tavar_nomi, MijozTavar, Tavar_rasmiylashtirish, Comment, Kassa


class TavarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tavar
        fields = '__all__'


class TavarnomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tavar_nomi
        fields = '__all__'


class MijozTavarSerializer(serializers.ModelSerializer):
    class Meta:
        model = MijozTavar
        fields = '__all__'


class TavarRasmiylashtirishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tavar_rasmiylashtirish
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class KassaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kassa
        fields = '__all__'
