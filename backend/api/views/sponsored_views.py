from rest_framework import viewsets
from core.models.social import SponsoredContent
from api.serializers import SponsoredContentSerializer
from rest_framework.permissions import AllowAny

class SponsoredContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SponsoredContent.objects.filter(is_active=True).order_by('?')
    serializer_class = SponsoredContentSerializer
    permission_classes = [AllowAny] 