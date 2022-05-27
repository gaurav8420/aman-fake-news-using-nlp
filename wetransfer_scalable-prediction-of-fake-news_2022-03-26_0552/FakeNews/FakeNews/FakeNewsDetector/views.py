from django.shortcuts import render
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from textblob import TextBlob
import re
import nltk

global name

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def UploadNews(request):
    if request.method == 'GET':
       return render(request, 'UploadNews.html', {})

def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('t1', False)
      password = request.POST.get('t2', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Login.html', context)

def UploadNewsDocument(request):
    global name
    if request.method == 'POST' and request.FILES['t1']:
        output = ''
        myfile = request.FILES['t1']
        fs = FileSystemStorage()
        name = str(myfile)
        filename = fs.save(name, myfile)
        context= {'data':name+' news document loaded'}
        return render(request, 'UploadNews.html', context)

def getQuotes(paragraph): #checking paragraph contains quotes or not
    score = 0
    match = re.findall('(?:"(.*?)")', paragraph)
    if match:
        score = len(match)
    return score    

def checkVerb(paragraph): #checking paragraph contains verbs or not
    score = 0
    b = TextBlob(paragraph)
    list = b.tags
    for i in range(len(list)):
        arr = str(list[i]).split(",")
        verb = arr[1].strip();
        verb = verb[1:len(verb)-2]
        if verb == 'VBG' or verb == 'VBN' or verb == 'VBP' or verb == 'VBD':
            score = score + 1
    return score

def nameEntities(paragraph): #getting names from paragraphs
    score = 0
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(paragraph))):
      if hasattr(chunk, 'label'):
          name = ' '.join(c[0] for c in chunk)
          score = score + 1
    return score      

def naiveBayes(quotes_score, verb_score, name, paragraph): #Naive Bayes to calculate score
    score = quotes_score + verb_score + name
    arr = nltk.word_tokenize(paragraph)
    total = (score/len(arr) * 10)
    return total

def DetectorAlgorithm(request): #detector and classifier algorithm
    global name
    if request.method == 'GET':
       strdata = '<table border=1 align=center width=100%><tr><th>News Text</th><th>Classifier Detection Result</th><th>Fake Rank Score</th></tr><tr>'
       with open(name, "r") as file:
          for line in file:
             line = line.strip('\n')
             line = line.strip()
             quotes_score = getQuotes(line)
             verb_score = checkVerb(line)
             entity_name = nameEntities(line)
             score = naiveBayes(quotes_score, verb_score, entity_name, line)
             if score > 0.90:
                strdata+='<td>'+line+'</td><td>Real News</td><td>'+str(score)+'</td></tr>'
             else:
                strdata+='<td>'+line+'</td><td>Fake News</td><td>'+str(score)+'</td></tr>'
   
    context= {'data':strdata}
    return render(request, 'ViewFakeNewsDetector.html', context)