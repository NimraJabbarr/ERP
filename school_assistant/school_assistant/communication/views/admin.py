"""
COMMUNICATION -- ADMIN-ROLE VIEWS
====================================
"""

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin
from communication.models import Notification, MediaCampaignLog
from communication.serializers.admin import NotificationSerializer, MediaCampaignLogSerializer


class NotificationListView(generics.ListAPIView):
    """
    GET /api/support/notifications
    Shared by every role in practice (each user sees their own), but the
    underlying view is generic -- Dev B's teacher/student/parent urls can
    point at this same view; it already filters by the logged-in user.
    """
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by("-created_at")


class UnreadNotificationListView(generics.ListAPIView):
    """GET /api/notifications/unread"""
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user, is_read=False).order_by("-created_at")


class MarkNotificationReadView(APIView):
    """PUT /api/notifications/read/{id}"""

    def put(self, request, id):
        Notification.objects.filter(id=id, receiver=request.user).update(is_read=True)
        return Response({"detail": "Marked as read."})


class MarkAllNotificationsReadView(APIView):
    """PUT /api/notifications/read-all"""

    def put(self, request):
        Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)
        return Response({"detail": "All notifications marked as read."})


class MediaCampaignViewSet(viewsets.ModelViewSet):
    """GET/POST /api/admin/campaigns -- drafts created by the Media Bot, reviewed/published by Admin."""

    queryset = MediaCampaignLog.objects.all().order_by("-created_at")
    serializer_class = MediaCampaignLogSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by_admin=self.request.user)


class PublishCampaignView(APIView):
    """
    POST /api/admin/campaigns/publish
    Pushes a drafted post to Make.com's webhook for Facebook/LinkedIn.
    The actual HTTP call to Make.com is a TODO -- wire it up once the
    Make.com scenario URL is ready; for now this just flips the status.
    """
    permission_classes = [IsAdmin]

    def post(self, request):
        campaign_id = request.data.get("campaign_id")
        campaign = MediaCampaignLog.objects.filter(id=campaign_id).first()
        if not campaign:
            return Response({"detail": "Campaign not found."}, status=404)

        # TODO: replace with an actual requests.post(MAKE_COM_WEBHOOK_URL, ...)
        # call once the Make.com scenario is configured. Set status="failed"
        # if that call errors, instead of assuming success like below.
        campaign.status = "published"
        campaign.save()
        return Response({"detail": "Campaign published.", "status": campaign.status})


class CampaignLogListView(generics.ListAPIView):
    """GET /api/admin/campaigns/logs"""
    queryset = MediaCampaignLog.objects.all().order_by("-created_at")
    serializer_class = MediaCampaignLogSerializer
    permission_classes = [IsAdmin]