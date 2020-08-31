from rest_framework import serializers

from dj_rest_auth.serializers import UserDetailsSerializer

from .models import CustomUser as User

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		depth = 1
		model = User
		depth = 1
		 #Add the other columns from the model when required
		fields = ('id', 'email', 'name', 'phone', 'site_id', 'is_creator', 'bio', 'rating', 'members',
		          'followers', 'earning', 'profession', 'location', 'member_since', 'picture',)
		read_only_fields = ['email', 'rating', 'members', 'followers', 'earning', 'member_since',]

class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserSerializer()

# class UserSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User

#We need UserDetailsSerializer class