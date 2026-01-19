from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, RegisterSerializer
from .permissions import IsOwner, IsProjectOwner

# List & Create Projects
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return projects owned by the logged-in user
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign logged-in user as owner
        serializer.save(owner=self.request.user)

# Retrieve, Update, Delete a Project
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Only allow owner to access
        return Project.objects.filter(owner=self.request.user)

# List & Create Tasks under a Project
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        # Only tasks in projects owned by logged-in user
        return Task.objects.filter(
            project__id=project_id,
            project__owner=self.request.user
        )

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        serializer.save(project_id=project_id)

# Retrieve, Update, Delete a Task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]

    def get_queryset(self):
        # Only tasks in projects owned by the user
        return Task.objects.filter(project__owner=self.request.user)


# Register API
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
