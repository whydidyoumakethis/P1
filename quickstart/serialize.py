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
    year = serializers.IntegerField()
    semester = serializers.ChoiceField(choices=Rating._meta.get_field('semester').choices)

    user_display = serializers.SerializerMethodField(read_only=True)
    professor_display = serializers.SerializerMethodField(read_only=True)
    module_display = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Rating
        fields = ['id', 'professor', 'module', 'year', 'semester','rating', 'created_at', 'user_display', 'professor_display', 'module_display']
    
    def create(self, validated_data):
        
        request = self.context.get('request')
        user = request.user
        professor_code = validated_data.pop('professor')
        module_code = validated_data.pop('module')
        year = validated_data.pop('year')
        semester = validated_data.pop('semester')

        professor = Professor.objects.get(code=professor_code)
        module = Module.objects.get(code=module_code)

        rating = Rating.objects.create(user=user, professor=professor, module=module, year=year, semester=semester, **validated_data)
        return rating


    
    def get_user_display(self, obj):
        return obj.user.username
    def get_professor_display(self, obj):
        return obj.professor.code
    def get_module_display(self, obj):
        return obj.module.code
