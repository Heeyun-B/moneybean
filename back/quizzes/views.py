from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Quiz, Attendance
from .serializers import QuizSerializer

class TodayQuizView(APIView):
    def get(self, request):
        try:
            quiz_count = Quiz.objects.count()
            if quiz_count == 0:
                return Response({"error": "문제가 없습니다."}, status=404)
            
            day_of_year = timezone.now().timetuple().tm_yday
            index = day_of_year % quiz_count
            quiz = Quiz.objects.all().order_by('id')[index]
            
            has_attended = False
            if request.user.is_authenticated:
                has_attended = Attendance.objects.filter(
                    user=request.user, 
                    quiz=quiz,
                    created_at=timezone.now().date() 
                ).exists()
            
            serializer = QuizSerializer(quiz)
            data = serializer.data
            data['has_attended'] = has_attended
            
            return Response(data)
        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            return Response({"error": str(e)}, status=500)

class AttendanceView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        quiz_id = request.data.get('quiz_id')
        today = timezone.now().date()
        
        if Attendance.objects.filter(user=request.user, created_at=today).exists():
            return Response({"message": "이미 참여했습니다."}, status=400)
            
        Attendance.objects.create(user=request.user, quiz_id=quiz_id, created_at=today)
        return Response({"message": "출석체크 완료!"}, status=status.HTTP_201_CREATED)