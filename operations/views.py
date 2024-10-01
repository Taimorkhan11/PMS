from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer, CreateTaskSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

#####################################################
# This signup api register the user in our database #
# in payload we just sent username, email, password #
# Created_at:  October 1, 2024                      #
# Update_at:                                        #
#####################################################


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED) # we can change the response as well
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#####################################################
# This api perform crud operation on Project Model  #
# Create, Retrive, Update, Delete and get list of   #
# all object. We can modify the behaviour according #
# to requierment.                                   #
# Created_at:  October 1, 2024                      #
# Update_at:                                        #
#####################################################


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        requested_user = request.user.id
        if requested_user not in  request.data['users']:
            request.data['users'].append(requested_user)
        serializer = self.get_serializer(data=request.data) # we can also use serializer_class here
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['admin_id'] = requested_user
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.admin == request.user:
            project.is_deleted = True
            project.save()
            return Response({"Message": f"You successfuly deleted your {project.name} porject."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Message": f"Only admin have access to delete this porject."}, status=status.HTTP_400_BAD_REQUEST)


#####################################################
# This api perform crud operation on Task Model     #
# Create, Retrive, Update, Delete and get list of   #
# all object. We can modify the behaviour according #
# to requierment. Only member of group create task  #
#  Only Admin can delete task, memeber of group     #
# update the task progress, name and title etc      #
# In this we can get project details as well.       #
#                                                   #
# Created_at:  October 1, 2024                      #
# Update_at:                                        #
#####################################################


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(is_deleted=False)
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        project_id = request.data['project']
        project_instance = Project.objects.filter(is_deleted=False, id=project_id)
        if project_instance:
            if request.user in project_instance.values("users"):
                serializer = CreateTaskSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return Response({"Message": f"You don't have permission to create task because you are not member of project."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": f"Project not avaiable for creating new task."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if task.project.admin == request.user:
            task.is_deleted = True
            task.save()
            return Response({"Message": f"You successfuly deleted your {task.name} task."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Message": f"You don't have permission to delete this task. Only Project Manager delete this task."}, status=status.HTTP_400_BAD_REQUEST)
