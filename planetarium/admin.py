from django.contrib import admin
from .models import (PlanetariumDome,
                     AstronomyShow,
                     ShowTheme,
                     ShowSession,
                     Reservation,
                     Ticket,
                     )


admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(Reservation)
admin.site.register(Ticket)
