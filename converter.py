import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XtraROMs.settings')

# Configure Django
django.setup()

from main.models import Blog, UserProfile
import requests
import json

def second():
    blogs = Blog.objects.all()

    for blog in blogs:
        text = requests.get("https://best-project-ashy.vercel.app/api/markdown/", {'text': blog.description})
        processed_text = text.json().get('processed_text')
        blog.description = processed_text
        blog.save()
    
def first():
    with open("out.json", "r") as file:
        data = json.load(file)
        
        for item in data:
            blog = Blog(
                id=item['id'],
                title=item['title'],
                description=item['description'],
                date=item['date'],
                link=item['link'],
                written_by=item['written_by']
            )
            blog.save
            
def third():
    user = UserProfile.objects.all()
    
    for pfp in user:
        if pfp.profile_picture == None:
            pfp.profile_picture == "C:/Users/siddh/OneDrive/Desktop/XtraROMs/main/static/images/akatsuki_logo.png"
        pfp.save
    
third()