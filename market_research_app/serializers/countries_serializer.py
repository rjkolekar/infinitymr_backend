from rest_framework import serializers

from market_research_app.models import Countries


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = "__all__"
