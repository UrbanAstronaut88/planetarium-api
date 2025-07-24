from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from planetarium.models import (PlanetariumDome,
                                AstronomyShow,
                                ShowTheme,
                                ShowSession,
                                Reservation,
                                Ticket
                                )
from planetarium.serializers import (PlanetariumDomeSerializer,
                                     AstronomyShowSerializer,
                                     ShowThemeSerializer,
                                     ShowSessionSerializer,
                                     ReservationSerializer,
                                     TicketSerializer
                                     )


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [permissions.AllowAny]


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = [permissions.AllowAny]


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [permissions.AllowAny]


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["get"], url_path="available-seats")
    def available_seats(self, request, pk=None):
        session = self.get_object()
        dome = session.planetarium_dome

        # all seats
        all_seats = set(
            (row, seat)
            for row in range(1, dome.rows + 1)
            for seat in range(1, dome.seats_in_row + 1)
        )

        # taken seats by tickets
        taken_seats = set(
            session.tickets.values_list("row", "seat")
        )

        # available seats
        available = sorted(list(all_seats - taken_seats))

        return Response({
            "show_session": session.id,
            "available_seats": available,
        })

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
