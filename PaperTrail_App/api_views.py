from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Document, Annotations, User
from .serializers import (
    AnnotationsSerializer,
    DocumentDetailsSerializer,
    SharedDocUserDetailsSerializer,
)


@api_view(["GET"])
def get_annotations(request, doc_id):
    try:
        document = get_object_or_404(Document, pk=doc_id)
    except Http404:
        return Response(
            {"annos": []},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = AnnotationsSerializer(data=document.annotations.all(), many=True)
    serializer.is_valid()  # Ensre data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"annos": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_documents(request):
    documents = request.user.docs.all().order_by("-created")
    serializer = DocumentDetailsSerializer(data=documents, many=True)
    serializer.is_valid()  # Ensure data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"docs": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def share_with(request):
    if request.method == "POST":
        data = request.data
        username = data.get("username")
        doc_id = data.get("docID")
        if not username or not doc_id:
            return Response(
                {"message": "Username and document ID are required.", "error": True},
                status=status.HTTP_202_ACCEPTED,
            )
        try:
            document = get_object_or_404(Document, id=doc_id)
            user = get_object_or_404(User, username=username)
        except:
            return Response(
                {"message": "User/Document was not found.", "error": True},
                status=status.HTTP_202_ACCEPTED,
            )
        if user == request.user:
            return Response(
                {
                    "message": "You can not add yourself. Are you sure what are you doing?",
                    "error": True,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        if user in document.shared_with.all():
            return Response(
                {
                    "message": "Document is already shared with this user.",
                    "error": True,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        document.shared_with.add(user)
        return Response(
            {
                "message": f"Document successfully shared with {user.username}.",
                "error": True,
            },
            status=status.HTTP_200_OK,
        )

    return Response(
        {"message": "Method not allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@api_view(["GET"])
def get_share_docs(request):
    documents = request.user.shared_docs.all().order_by("-created")
    serializer = DocumentDetailsSerializer(data=documents, many=True)
    serializer.is_valid()  # Ensure data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"docs": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_shared_list(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    print(document)
    if not document or (
        request.user != document.owner
        and not request.user in document.shared_with.all()
    ):
        return Response(
            {"message": "Invalid document", "users": []},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = SharedDocUserDetailsSerializer(
        data=document.shared_with.all(), many=True
    )
    serializer.is_valid()  # Ensure data is valid before serialization
    serialized_data = serializer.data  # Access serialized data

    return Response(
        {"message": "Retrieved successfully.", "users": serialized_data},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def remove_access(request):
    if request.method == "POST":
        data = request.data
        user_id = data.get("userID")
        doc_id = data.get("docID")
        if not user_id or not doc_id:
            return Response(
                {"message": "Username and document ID are required."},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            document = get_object_or_404(Document, id=doc_id)
            user = get_object_or_404(User, pk=user_id)
        except:
            return Response(
                {"message": "User/Document was not found."},
                status=status.HTTP_202_ACCEPTED,
            )
        if not user in document.shared_with.all():
            return Response(
                {"message": "User/Document was not found."},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            document.shared_with.remove(user)
            return Response(
                {"message": "Successfully removed the user"},
                status=status.HTTP_200_OK,
            )
    return Response(
        {"message": "Invalid method."},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(["POST"])
def create_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data
        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            return Response(
                {"message": "Method not allowed", "anno_id": -1},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        try:
            page_number = annotation_data["pageNumber"]
        except:
            page_number = 1

        annotation_instance = Annotations.objects.create(
            body_value=annotation_data["annotation"]["body"][0]["value"],
            target_selector_value=annotation_data["annotation"]["target"]["selector"][
                "value"
            ],
            doc_id=document,
            annotator=request.user,
            page_number=page_number,
        )
        annotation_instance.save()
        return Response(
            {
                "message": "Annotation created successfully",
                "anno_id": annotation_instance.pk,
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def update_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data

        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            print("Doc not found")
            return Response(
                {"message": "No such document found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )

        annotation_instance = get_object_or_404(
            Annotations, id=annotation_data["annotation"]["id"]
        )
        if not annotation_instance:
            print("Annotation not found")
            return Response(
                {"message": "No such annotation found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )
        annotation_instance.body_value = annotation_data["annotation"]["body"][0][
            "value"
        ]
        annotation_instance.target_selector_value = annotation_data["annotation"][
            "target"
        ]["selector"]["value"]
        annotation_instance.save()
        return Response(
            {
                "message": "Annotation updated successfully",
                "anno_id": annotation_instance.pk,
            },
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def delete_annotation(request):
    if request.method == "POST":
        # Assuming you receive annotation data in the request data
        annotation_data = request.data
        document = get_object_or_404(Document, id=annotation_data["doc_id"])
        if not document:
            return Response(
                {"message": "No such document found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )

        annotation_instance = get_object_or_404(
            Annotations, id=annotation_data["annotation"]["id"]
        )
        if not annotation_instance:
            return Response(
                {"message": "No such annotation found.", "anno_id": -1},
                status=status.HTTP_400_BAD_REQUEST,
            )
        annotation_instance.delete()
        return Response(
            {"message": "Annotation deleted successfully"},
            status=status.HTTP_202_ACCEPTED,
        )
    else:
        return Response(
            {"message": "Method not allowed", "anno_id": -1},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


@api_view(["POST"])
def delete_docfile(request):
    if request.method == "POST":

        doc_file_id = request.data["doc_id"]
        document = get_object_or_404(Document, id=doc_file_id)
        if document.owner == request.user:
            document.delete()
            return Response(
                {"message": "Document deleted successfully."},
                status=status.HTTP_202_ACCEPTED,
            )

    return Response(
        {"message": "Method not allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@api_view(["POST"])
def search_query(request):
    if request.method == "POST":
        data = request.data
        query = data.get("query")
        checked_values = data.get("checkboxValues")

        if not query:
            return Response(
                {"message": "Query is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Initialize an empty list to store search results
        search_results = []

        if not checked_values or "Document" in checked_values:
            # Search in Document model
            document_results = Document.objects.filter(
                Q(doc_name__icontains=query, owner=request.user)
                | Q(owner__username__icontains=query, owner=request.user)
                | Q(doc_type__icontains=query, owner=request.user)
            )
            search_results.extend(document_results)

        # Search in Annotations model if "Annotation" is checked
        if "Annotation" in checked_values:
            # Get all annotations of the current user
            user_annotations = request.user.annotations.all()

            # Filter annotations based on the query
            filtered_annotations = user_annotations.filter(
                Q(body_value__icontains=query)
            )

            # Add associated documents to the search results
            for annotation in filtered_annotations:
                search_results.append(annotation.doc_id)

            # Search in shared documents annotations
            shared_documents = request.user.shared_docs.all()
            for shared_doc in shared_documents:
                shared_annotations = shared_doc.annotations.filter(
                    Q(body_value__icontains=query)
                    | Q(annotator__username__icontains=query)
                )

                # Add associated shared documents to the search results
                for annotation in shared_annotations:
                    search_results.append(annotation.doc_id)

            # Search in user own documents but someone else annotations
            own_documents_with_other_people_annotations = request.user.docs.all()

            for shared_doc in own_documents_with_other_people_annotations:
                shared_annotations = shared_doc.annotations.filter(
                    Q(body_value__icontains=query)
                    | Q(annotator__username__icontains=query)
                )

                # Add associated shared documents to the search results
                for annotation in shared_annotations:
                    search_results.append(annotation.doc_id)

        # Search in Shared documents if "Shared" is checked
        if "Shared" in checked_values:
            shared_documents = request.user.shared_docs.filter(
                Q(doc_name__icontains=query)
                | Q(owner__username__icontains=query)
                | Q(doc_type__icontains=query)
            )
            search_results.extend(shared_documents)

        # Serialize the search results
        serializer = DocumentDetailsSerializer(search_results, many=True)

        return Response({"message": "Successfull Retrieval.", "docs": serializer.data})

    return Response(
        {"message": "Method not allowed"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
