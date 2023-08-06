# PersonalAssistant

A module for making a voice assistant
Quick start guide:
```
import PersonalAssistant

# Get your news api key on newsapi website. And give your api key in the parameter 'news_api_key'
# Disbale less secure apps in your gmail

ass = PersoanlAssistant.Assistant(
    name='Jarvis', # Name of your assistant
    voice=0, 
    news_api_key='your-news-api-key', # Your news api key
    your_google_pass='your-gmail-password', # You email password
    your_google_email='your-gmail-email', # Your email
)
ass.start # Starts your assistant
```