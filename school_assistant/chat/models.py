"""
CHAT APP
========
AI chatbot conversation storage. Real-time message delivery is handled
separately by a Channels WebSocket consumer (to be added later in
chat/consumers.py and chat/routing.py) -- this file only defines the
persistence layer.

Cross-app references used in this file:
- ChatSession.user -> accounts.User
- ChatSession.active_child -> accounts.StudentProfile
"""

from django.db import models


class ChatSession(models.Model):
    """
    One conversation thread. Only Admin actually chooses between the 10
    specialized bot types below (the "Bot Hub"); Teacher/Student/Parent
    sessions default to "general" since the spec only gives Admin a hub
    of multiple assistants -- the other three roles get one scoped bot each.
    """

    BOT_TYPE_CHOICES = (
        ("maintenance", "Maintenance & Help Desk Bot"),
        ("fee", "Fee Bot"),
        ("media", "Media Bot"),
        ("assignment", "Assignment Bot"),
        ("exam", "Exam Bot"),
        ("attendance", "Attendance & Compliance Bot"),
        ("certificate", "Certificates Bot"),
        ("scholarship", "Scholarship Bot"),
        ("inventory", "Inventory Bot"),
        ("event", "Event Bot"),
        ("general", "General Assistant"),  # used by Teacher / Student / Parent
    )

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="chat_sessions")
    bot_type = models.CharField(max_length=20, choices=BOT_TYPE_CHOICES, default="general")
    title = models.CharField(max_length=200, blank=True)  # auto-filled from the first user message

    # Only meaningful when user.role == Parent -- tracks which child the
    # conversation is currently scoped to, matching the child-toggle on
    # the Parent Dashboard (Page 31).
    active_child = models.ForeignKey(
        "accounts.StudentProfile", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


class ChatMessage(models.Model):
    ROLE_CHOICES = (("user", "user"), ("assistant", "assistant"))

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
