import json
from . import models

with open("blog.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
for entry in data:
    blog = models.Blog(
        title=entry['title'],
        description=entry['description'],
        written_by=entry['written_by'],
        date=entry['date'],
        link=entry['related_link']
    )
    blog.save()