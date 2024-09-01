# Important part for API serialization

# https://www.django-rest-framework.org/api-guide/fields/

from rest_framework import serializers

class GenerateTextSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=1000)


class Info_Bulk_Posting_Serializer(serializers.Serializer):
    keyword_list = serializers.CharField()
    website_id = serializers.CharField(max_length=500)
    youtubeapi_id = serializers.CharField(max_length=500, required=False, allow_blank=True)
    category = serializers.CharField(max_length=500, required=False, allow_blank=True)
    post_status = serializers.CharField(max_length=200)
    img_status = serializers.CharField(max_length=200)


# ----- After any change or add serializer field need to do database migrations -----
