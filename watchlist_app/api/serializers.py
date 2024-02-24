
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review
 
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    len_title = serializers.SerializerMethodField() #custom fields
    class Meta:
        model = WatchList
        fields = "__all__"

    def get_len_title(self, object):
        return len(object.title)
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"

    
    


















     #    fields = ['id', 'name', 'description', 'active']
     #    exclude = ('id',)

# def is_true_or_false(value):
#      if value != 'true' or value != 'false':
#           raise serializers.ValidationError(f'for active({value}) boolean values must be true or false')
#      else:
#           return value     

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField(validators=[is_true_or_false])#validators can be used instead of field level validation

#     def create(self, validated_data):
#          return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#          instance.name = validated_data.get('name', instance.name)
#          instance.description = validated_data.get('description', instance.description)
#          instance.active = validated_data.get('active', instance.active)
#          instance.save()
#          return instance 
    
#     #validation in DRF, called when ever the is_valid() method is used in the views
#     def validate(self, data):#object level validation
#          if data['name'] == data.get('description'):
#               raise serializers.ValidationError('title(name) and description should be different!')
#          else:
#               return data
    
#     def validate_name(self, value):#field level validation
#          if len(value) < 5:
#               raise serializers.ValidationError(f"{value} is not a valid name")
#          else:
#               return value
         