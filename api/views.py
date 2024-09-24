from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Contact, SpamReport
from .serializers import ContactSerializer, SpamReportSerializer, RegisterSerializer
from django.contrib.auth.models import User

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restricts the returned contacts based on the search query parameter,
        by filtering against 'name' or 'phone_number'.
        """
        queryset = super().get_queryset()
        query = self.request.query_params.get('q', None)
        
        if query:
            if query.isdigit():
                # Search by phone number
                return queryset.filter(phone_number__icontains=query)
            else:
                # Search by name (case insensitive)
                return queryset.filter(name__icontains(query))
        
        return queryset

    def perform_create(self, serializer):
        serializer.save()  # Optionally, you can add the user to the contact here


class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        phone_number = serializer.validated_data['phone_number']

        # Check if the phone number already exists in the spam report
        spam_report, created = SpamReport.objects.get_or_create(phone_number=phone_number)

        if created:
            # If a new spam report is created, set the spam count to 1
            spam_report.spam_count = 1
        else:
            # If the spam report exists, increment the spam count
            spam_report.spam_count += 1
        
        spam_report.save()  # Save the spam report with the updated spam count
        return Response({'message': 'Spam report created/updated successfully', 'spam_count': spam_report.spam_count})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_spam_count(self, request):
        """
        Custom action to retrieve the spam count for a particular phone number.
        """
        phone_number = request.query_params.get('phone_number')
        if phone_number:
            try:
                spam_report = SpamReport.objects.get(phone_number=phone_number)
                return Response({'spam_count': spam_report.spam_count})
            except SpamReport.DoesNotExist:
                return Response({'spam_count': 0, 'message': 'Phone number not reported as spam yet'}, status=404)
        return Response({'message': 'No phone number provided'}, status=400)


# Create a register view for handling user registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to access the registration endpoint
