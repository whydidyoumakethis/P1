from django.contrib.auth.models import User
from rest_framework import serializers

from quickstart.models import Module, Professor, Rating
from django.db.models import Avg


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']


############################################################################################################

class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = Professor
        fields = ['id', 'code','name', 'avg_rating']
    def get_avg_rating(self, obj):
        avg_rating = Rating.objects.filter(professor=obj).aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 2) if avg_rating else 0

class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    professors = ProfessorSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['name', 'code', 'year', 'semester', 'professors']


class RatingSerializer(serializers.ModelSerializer):
    professor = serializers.CharField(write_only=True)
    module = serializers.CharField(write_only=True)
    semester = serializers.ChoiceField(choices=Rating._meta.get_field('semester').choices)


    class Meta:
        model = Rating
        fields = ['id', 'professor', 'module', 'year', 'semester','rating', 'created_at']
    
    def create(self, validated_data):
        
        request = self.context.get('request')
        validated_data['user'] = request.user
        return Rating.objects.create(**validated_data)

    

