from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone, http
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from rest_framework import viewsets, mixins, status, renderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import TemplateHTMLRenderer, HTMLFormRenderer
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from django.shortcuts import render
from .forms import RegistrationForm


class EventView(viewsets.ReadOnlyModelViewSet):
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request, *args, **kwargs):
        queryset = Event.objects.filter(start_time__gte=timezone.now())
        if request.accepted_renderer.format == "html":
            return Response({'events': queryset}, template_name='event_list.html')
        serializer = EventSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)


class EventManage(viewsets.ModelViewSet):
    # permission_classes = [HasAPIKey]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RegistrationDetails(viewsets.ModelViewSet):
    # permission_classes = [HasAPIKey]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        event_id = self.request.query_params.get('event_id')
        queryset = Registration.objects.filter(event_id=event_id)
        return queryset


class RegistrationManage(viewsets.ModelViewSet):
    permission_classes = [HasAPIKey]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail_post_signup(request.data['event'], request.data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register_new(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrationForm()
            messages.success(request, 'You have been signed up for the event - checkout other events')
            send_mail_post_signup(request.POST.get('event'), request.POST.get('email'))
            return render(request, 'newRegistration.html', {'form': form}, status=status.HTTP_201_CREATED)
        else:
            return render(request, 'newRegistration.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST)
    return render(request, 'newRegistration.html', {'form': form})


def send_mail_post_signup(event_id, email_id):
    event = Event.objects.get(id=event_id)
    event_name = event.name
    count = Registration.objects.filter(event_id=event_id).count()
    subject = 'new Signup for event: ' + event_name + '( event_id: ' + event_id + ' )'
    body = 'The mailId signedUp: ' + email_id + "\n total signUps:" + str(count)
    send_mail(
        subject,
        body,
        settings.FROM_MAIL_ID,
        [settings.TO_MAIL_ID],
        fail_silently=False,
    )
