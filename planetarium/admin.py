from django.contrib import admin
from .models import (PlanetariumDome,
                     AstronomyShow,
                     ShowTheme
                     )


admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
