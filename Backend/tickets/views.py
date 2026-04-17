# tickets/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Avg
from django.db.models.functions import TruncDay

from .models import Ticket
from .serializers import TicketSeriliazer
from .tasks import process_ticket_task, send_ticket_confirmation_email
from .utils import classify_ticket   # ✅ Correct import


# ✅ List & Create
class TicketListCreateView(APIView):

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketSeriliazer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TicketSeriliazer(data=request.data)

        if serializer.is_valid():
            ticket = serializer.save()

            # Run tasks in background
            process_ticket_task.delay(ticket.id)
            send_ticket_confirmation_email.delay(ticket.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Update Ticket
class TicketDetailView(APIView):

    def patch(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response(
                {'error': "Ticket not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TicketSeriliazer(ticket, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Stats View
class TicketStatsView(APIView):

    def get(self, request):

        total_tickets = Ticket.objects.count()
        open_tickets = Ticket.objects.filter(status='open').count()

        daily_counts = (
            Ticket.objects
            .annotate(day=TruncDay('created_at'))
            .values('day')
            .annotate(count=Count('id'))
        )

        avg_tickets_per_day = daily_counts.aggregate(
            avg=Avg('count')
        )['avg']

        priority_counts = (
            Ticket.objects
            .values('priority')
            .annotate(count=Count('id'))
        )

        priority_breakdown = {
            item['priority']: item['count']
            for item in priority_counts
        }

        category_counts = (
            Ticket.objects
            .values('category')
            .annotate(count=Count('id'))
        )

        category_breakdown = {
            item['category']: item['count']
            for item in category_counts
        }

        data = {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "avg_tickets_per_day": avg_tickets_per_day,
            "priority_breakdown": priority_breakdown,
            "category_breakdown": category_breakdown,
        }

        return Response(data, status=status.HTTP_200_OK)


# ✅ Classification API
class TicketClassifyView(APIView):

    def post(self, request):
        description = request.data.get("description")

        if not description:
            return Response(
                {"error": "Description is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = classify_ticket(description)

        return Response(result, status=status.HTTP_200_OK)