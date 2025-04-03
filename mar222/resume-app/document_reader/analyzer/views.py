from django.shortcuts import render

# Create your views here.

import os
import openai
from rest_framework.response import Response
from rest_framework.decorators import api_view
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from django.core.files.uploadedfile import InMemoryUploadedFile



FORM_RECOGNIZER_ENDPOINT = "https://resume-reader-cp.cognitiveservices.azure.com/"
FORM_RECOGNIZER_KEY = "EPcNIyLAVJMqIktWB8pW3WoVITH9MmR4WSAdbKfN4TmPNASo78WUJQQJ99BDACYeBjFXJ3w3AAALACOG6AJB"

@api_view(['POST'])
def analyze_resume(request):
    try:
        print("Recieved files:", request.FILES)

        document = request.FILES.get('resume')
        
        if not document:
            return Response({"success": False, "error": "No resume file provided"}, status=400)

        # document_bytes = document.read() if isinstance(document, InMemoryUploadedFile) else None

        if isinstance(document, InMemoryUploadedFile):
            document_bytes = document.read()
        else:
            return Response({"success": False, "error": "Invalid file SILLY"}, status=400)

        client = DocumentAnalysisClient(FORM_RECOGNIZER_ENDPOINT, AzureKeyCredential(FORM_RECOGNIZER_KEY))

        poller = client.begin_analyze_document("prebuilt-document", document_bytes)
        result = poller.result()

        return Response({"success": True, "data": result}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

def refine_resume(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Analyze this resume and suggest improvements."},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]


# openai.api_key = os.getenv("3ZW726RSIvFfCPG3dzvXS0NSsF2dQDcezuzY2BLmPy2I1aWII3blJQQJ99BDACYeBjFXJ3w3AAALACOGsu1H")

@api_view(['POST'])
def chat_resume_analysis(request):
    try:
        resume_data = request.data.get("resume_data", {})
        user_question = request.data.get("question", "")

        if not resume_data or not user_question:
            return Response({"success": False, "error": "Missing resume data or question"}, status=400)

        system_message = f"Analyze this resume data: {resume_data} and answer the user's question."
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_question}
            ]
        )

        return Response({"success": True, "response": response["choices"][0]["message"]["content"]}, status=200)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)