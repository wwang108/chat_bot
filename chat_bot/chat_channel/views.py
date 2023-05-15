from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Campsite, Reservation, UserMessage
from .forms import ReservationForm, MessageForm
from django.http import JsonResponse
import subprocess
import json
from django.views.decorators.csrf import csrf_exempt
from langchain.embeddings.openai import OpenAIEmbeddings
from .response import CampingChatbot
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from langchain.chains import RetrievalQA
from langchain.llms import OpenAIChat
from langchain.vectorstores import DeepLake
import re

def format_code_blocks(api_response_text):
    # Search for code blocks wrapped in triple backticks
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    
    # Replace the triple backticks with HTML pre and code tags
    formatted_text = code_block_pattern.sub(r'<pre><code>\1</code></pre>', api_response_text)
    
    return formatted_text


# Create your views here.
# loader = TextLoader("./chat_channel/static/data/camp_knowledge.txt")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(
#     chunk_size=1000, separator="\n", chunk_overlap=0)
# documents = text_splitter.split_documents(documents)
os.environ['OPENAI_API_KEY'] = 
embeddings = OpenAIEmbeddings()
dataset_path = "chat_channel/my_deeplake/"
chat = CampingChatbot(dataset_path=dataset_path, embeddings=embeddings)



@login_required
def chatbot(request):
    form = MessageForm(request.POST or None)
    response_message = ''

    if request.method == 'POST' and form.is_valid():
        form_data = request.POST.dict()
        user_message = form_data.get('message')

        if user_message:
            response_message = chat.receive_message(user_message)
            print(response_message)
            formatted_text = format_code_blocks(response_message)
            response_message = formatted_text
            print(response_message)
        else:
            response_message = 'Hi, how can I help you?'

        return JsonResponse({'message': response_message}, safe=False)
    else:
        return render(request, 'chat_channel/chatbot.html', {'form': form})


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Log the user in.
#             login(request, user)
#             # Change 'home' to the name of the view you want to redirect the user to after signup
#             return redirect('home')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'chat_channel/signup.html', {'form': form})
