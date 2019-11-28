from django.http import HttpResponse, JsonResponse,QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Student
from .serializers import StudentSerializer
from .security import AESCipher
from .selenium import Selenium

# Create your views here.

@csrf_exempt
def student_list(request):
    if request.method == 'GET':
        students=Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = request.POST
        # _mutable = data._mutable
        # data._mutable = True
        # data['password'] =  AESCipher(data['s_id']).encrypt(data['password'])
        # data._mutable = _mutable
        serializer = StudentSerializer(data=data)

        if serializer.is_valid():        
            serializer.save()
            return JsonResponse({
                'result': 'Enrolled.',
                'pk' : serializer.data['pk']
            }, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = QueryDict(request.body)
        _mutable = data._mutable
        data._mutable = True
        data['password'] =  AESCipher(data['s_id']).encrypt(data['password'])
        data._mutable = _mutable
        serializer = StudentSerializer(student, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'result': 'Updated.'
            }, status=201)
        return HttpResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        student.delete()
        return JsonResponse({
                'result': 'Deleted.'
            }, status=201)
    return HttpResponse(status=404)            

@csrf_exempt
@require_POST
def student_enter(request):
    data = QueryDict(request.body)
    student = Student.objects.get(pk=data['pk'])
    student_password = AESCipher(student.s_id).decrypt(student.password)
    return Selenium(student.s_id, student_password).pk_action("enter", student.pk)

@csrf_exempt
@require_POST
def student_exit(request):
    data = QueryDict(request.body)
    student = Student.objects.get(pk=data['pk'])
    student_password = AESCipher(student.s_id).decrypt(student.password)
    return Selenium(student.s_id, student_password).pk_action("exit", student.pk)

@csrf_exempt
@require_POST
def manual_enter(request):
    data = QueryDict(request.body)
    student = Student.objects.get(s_id = data['s_id'])
    return Selenium(data['s_id'], data['password']).pk_action("enter", student.pk)

@csrf_exempt
@require_POST
def manual_exit(request):
    data = QueryDict(request.body)
    student = Student.objects.get(s_id = data['s_id'])
    return Selenium(data['s_id'], data['password']).pk_action("exit", student.pk)
