from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from user.models import User
from user.serializers import UserSerializer

class UsersViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """Постраничное получение кратких данных обо всех пользователях

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        return Response(self.serializer_class(self.queryset, many=True).data)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def current(self, request):
        """Здесь пользователь в зависимости от запроса может получить или изменить свои данные

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        return Response()

class AdminViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        """Постраничное получение кратких данных обо всех пользователях

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        return Response(self.serializer_class(self.queryset, many=True).data)

    def create(sefl, request):
        """Создание пользователя

        Здесь возможно занести в базу нового пользователя с минимальной информацией о нем

        Args:
            sefl ([type]): [description]
            request ([type]): [description]
        """

        return Response()

    def retrieve(self, request, pk=None):
        """Детальное получение информации о пользователе

        Здесь администратор может увидеть всю существующую пользовательскую информацию

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """
        return Response()

    def partial_update(self, request, pk=None):
        """Изменение информации о пользователе

        Здесь администратор может изменить любую информацию о пользователе

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """
        return Response()

    def destroy(self, request, pk=None):
        """Удаление пользователя

        Args:
            request ([type]): [description]
            pk ([type], optional): [description]. Defaults to None.
        """
        return Response()

class AuthViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Вход в систему

        После успешного входа в систему необходимо установить Cookies для пользователя

        Args:
            request ([type]): [description]
        """
        pass

    @action(detail=False, methods=['get'])
    def logout(self, request):
        """Выход из системы

        При успешном выходе необходимо удалить установленные Cookies

        Args:
            request ([type]): [description]
        """
        pass