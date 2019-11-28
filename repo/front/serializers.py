from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.Serializer):
    pk = serializers.IntegerField(label='PK', read_only=True)
    name = serializers.CharField(required=False, allow_blank=True,max_length=50)
    s_id = serializers.CharField(required=True, allow_blank=False, max_length=50)
    password = serializers.CharField(required=True, allow_blank=False, max_length=150)
    
    class Meta:
        model = Student
        fields= ['pk', 'name', 's_id', 'password']

    def create(self, validated_data):
        
        return Student.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance