from rest_framework import serializers
from academics.models import Grade, Assignment, AssignmentSubmission

class GradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.subject_name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.full_name", read_only=True)

    class Meta:
        model = Grade
        fields = [
            "id", "subject", "subject_name", "exam_type",
            "obtained_marks", "total_marks", "exam_date", "teacher_name"
        ]
        read_only_fields = ["id", "subject_name", "teacher_name"]


class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.subject_name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.full_name", read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id", "title", "description", "due_date",
            "attachment_url", "subject_name", "teacher_name"
        ]
        read_only_fields = ["id", "subject_name", "teacher_name"]


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)

    # Prevent students from self-grading.
    marks = serializers.IntegerField(read_only=True)
    feedback = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id",
            "assignment",
            "assignment_title",
            "file_url",
            "submitted_at",
            "marks",
            "feedback",
        ]
        read_only_fields = ["id", "submitted_at", "assignment_title", "marks", "feedback"]

