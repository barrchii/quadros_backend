from rest_framework import serializers



class SendCodeSerializer (serializers.Serializer):
    email = serializers.EmailField()



class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)