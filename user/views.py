from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.paginations import CustomAdminPagination, CustomPagination
from user.serializers import (UserCreateSerializer, UserFullSerializer,
                              UserLoginSerializer, UserSerializer,
                              UserShortSerializer)


class UsersViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("page", int, required=True),
            OpenApiParameter("size", int, required=True),
        ],
        responses={
            200: UserShortSerializer,
        })
    def list(self, request):
        """Постраничное получение кратких данных обо всех пользователях
        """
        pagination = self.pagination_class()
        qs = pagination.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(qs, many=True)
        return pagination.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def current(self, request):
        """Здесь пользователь в зависимости от запроса может получить или изменить свои данные
        """
        if request.method == 'GET':
            return Response(self.serializer_class(request.user).data)
        elif request.method == 'PATCH':
            serializer = self.serializer_class(
                request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(self.serializer_class(request.user).data)
            else:
                print(serializer.errors)
                return JsonResponse({"detail": serializer.errors}, status=422)


class AdminViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserFullSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomAdminPagination

    @extend_schema(
        parameters=[
            OpenApiParameter("page", int, required=True),
            OpenApiParameter("size", int, required=True),
        ],)
    def list(self, request):
        """Постраничное получение кратких данных обо всех пользователях
        """
        qs = self.pagination_class.paginate_queryset(self.queryset, request)
        serializer = self.serializer_class(qs, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    @extend_schema(
        request=UserCreateSerializer,
        responses={201: UserFullSerializer}
    )
    def create(self, request):
        """Создание пользователя
        """

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(self.serializer_class(user).data)
        else:
            print(serializer.errors)
            return JsonResponse({"detail": serializer.errors}, status=422)

    @extend_schema(
        responses={200: UserFullSerializer}
    )
    def retrieve(self, request, pk):
        """Детальное получение информации о пользователе

        Здесь администратор может увидеть всю существующую пользовательскую информацию
        """
        user = get_object_or_404(self.queryset, pk=pk)
        return Response(self.serializer_class(user).data)

    @extend_schema(
        request=UserFullSerializer,
        responses={200: UserFullSerializer}
    )
    def partial_update(self, request, pk=None):
        """Изменение информации о пользователе

        Здесь администратор может изменить любую информацию о пользователе
        """
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(self.serializer_class(user).data)
        else:
            print(serializer.errors)
            return JsonResponse({"detail": serializer.errors}, status=422)

    @extend_schema(
        responses={
            204: None,
            401: {"code": "string"},
            403: {"code": "string"},
        }
    )
    def destroy(self, request, pk=None):
        """Удаление пользователя c id = pk
        """
        user = get_object_or_404(self.queryset, pk=pk)
        user.delete()
        return JsonResponse(None)


class AuthViewSet(viewsets.ViewSet):

    serializer_class = UserSerializer

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            201: UserSerializer,
            400: {"code": 400, "message": "Wrong body"},
            401: {"code": 401, "message": "Wrong email or password"}},
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Вход в систему

        После успешного входа в систему необходимо установить Cookies для пользователя
        """
        if not request.data:
            return JsonResponse({"code": 400, "message": "Wrong body"}, status=400)

        data = request.data
        try:
            user = authenticate(email=data["email"], password=data["password"])
            if user is not None:
                login(request, user)
                return Response(self.serializer_class(user).data)
            else:
                return JsonResponse({"code": 401, "message": "Wrong email or password"}, status=401)
        except KeyError:
            return JsonResponse({"code": 422, "message": "Wrong body"}, status=422)

    @extend_schema(
        responses={200: str},
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Выход из системы

        При успешном выходе необходимо удалить установленные Cookies
        """
        logout(request)
        return JsonResponse({"msg": "Successful logout"})
