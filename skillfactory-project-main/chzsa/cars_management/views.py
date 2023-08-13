from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car, Maintenance, Reclamation
from .serializers import CarSerializer, ServiceSerializer, ClaimSerializer


def create_groups(sender, **kwargs):
    if not Group.objects.create(name='client'):
        Group.objects.create(name='client')

    if not Group.objects.create(name='service_organization'):
        Group.objects.create(name='service_organization')

    if not Group.objects.create(name='manager'):
        Group.objects.create(name='manager')

def is_client(user):
    return user.groups.filter(name='client').exists()

def is_service_organization(user):
    return user.groups.filter(name='service_organization').exists()

def is_manager(user):
    return user.groups.filter(name='manager').exists()


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def car_list(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def car_detail(request):
    factory_number = request.GET.get('factory_number')
    try:
        car = Car.objects.get(factory_number=factory_number)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким заводским номером нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_service_organization)
def service_list(request, id):
    try:
        car = Car.objects.get(id=id)
        services = Maintenance.objects.filter(car=car)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_manager)
def claim_list(request, id):
    try:
        car = Car.objects.get(id=id)
        claims = Reclamation.objects.filter(car=car)
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)
    except Car.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


def login(request):
    # ToDo: Put actual template here
    return render(request, 'login.html')