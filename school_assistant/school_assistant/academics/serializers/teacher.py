from rest_framework import serializers
from academics.models import Grade, Assignment, AssignmentSubmission

class TeacherGradeEntrySerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = Grade
        fields = [
            "id", "student", "student_name", "subject",
            "exam_type", "obtained_marks", "total_marks", "exam_date"
        ]


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = [
            "id", "title", "description", "due_date",
            "attachment_url", "subject", "class_section"
        ]


class TeacherAssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id", "assignment", "student", "student_name",
            "file_url", "submitted_at", "marks", "feedback"
        ]
