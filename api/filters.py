from django_filters import rest_framework as filters
from . import models


class PostFilter(filters.FilterSet):
    publish_date_after = filters.DateFilter(field_name='publish_date', lookup_expr='gte')
    publish_date_before = filters.DateFilter(field_name='publish_date', lookup_expr='lte')
    
    class Meta:
        model = models.Post
        fields = ['publish_date_after', 'publish_date_before']


class CommentFilter(filters.FilterSet):
    publish_date_after = filters.DateFilter(field_name='published_date', lookup_expr='gte')
    publish_date_before = filters.DateFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = models.Comment
        fields = ['publish_date_after', 'publish_date_before']