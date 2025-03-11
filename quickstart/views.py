from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, status  # Added status import
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate, login as django_login
from quickstart.serialize import UserSerializer
from quickstart.models import Professor, Module, Rating
from quickstart.serialize import ModuleSerializer, ProfessorSerializer, RatingSerializer
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.middleware.csrf import get_token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],  # Optional email
                password=serializer.validated_data['password']
            )
        return Response(
            UserSerializer(user, context={'request': request}).data,
            status=status.HTTP_201_CREATED  # Fixed status import
        )
    


#################################################################################

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def token_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        django_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout(request):

    if request.auth is None:
        django_logout(request)
        return Response({'message': 'User logged out successfully'})
    
    try:
        request.user.auth_token.delete()
        return Response({'message': 'User logged out successfully'})
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=400)
    

class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    def list(self, request, *args, **kwargs):
        professors = Professor.objects.all()
        data = []

        for professor in professors:
            avg_rating = Rating.objects.filter(professor=professor).aggregate(Avg('rating'))['rating__avg']
            avg_rating = round(avg_rating, 2) if avg_rating else 0
            stars = "*" * round(avg_rating)
            data.append({
                'id': professor.id,
                'code': professor.code,
                'name': professor.name,
                'avg_rating': avg_rating,
                'stars': stars
            })
        return Response(data)
    
class professorModuleRatingViewSet(viewsets.ModelViewSet):
  
  def retrieve(self, request, professor_code=None, module_code=None):
      try:
            professor = Professor.objects.get(code=professor_code)
            module = Module.objects.get(code=module_code)
            avg_rating = Rating.objects.filter(professor=professor, module=module).aggregate(Avg('rating'))['rating__avg']
            avg_rating = round(avg_rating, 2) if avg_rating else 0
            stars = "*" * round(avg_rating)
            return Response({
                'professor_code': professor.code,
                'professor': professor.name,
                'module_code': module.code,
                'module': module.name,
                'avg_rating': avg_rating,
                'stars': stars
            })
      except (Professor.DoesNotExist, Module.DoesNotExist):
            return Response({
                'error': 'Professor or Module does not exist'
            }, status=404)
      
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
