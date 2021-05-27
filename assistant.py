import speech_recognition as sr 
import playsound # to play saved mp3 file 
from gtts import gTTS # google text to speech 
import os # to save/open files 
import wolframalpha # to calculate strings into formula 
from selenium import webdriver # to control browser operations
import sounddevice as sd
import wavio as wv
from apiclient.discovery import build
from pyaudio import PyAudio
from newspaper import Article


num=1;

def youtube(query):
	DEVELOPER_KEY = "you can take it from google and enter that key here";
	YOUTUBE_API_SERVICE_NAME = "youtube";
	YOUTUBE_API_VERSION = "v3";
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                                      developerKey = DEVELOPER_KEY);
	search_keyword = youtube.search().list(q = query, part = "id, snippet", 
                                               maxResults = 10).execute();
	URLS = f"https://www.youtube.com/watch?v={search_keyword['items'][0]['id']['videoId']}";
	return(URLS);


def machine_speak(naam):
	global num;
	num+=1;
	print("Computer : ",naam);
	language='en'
	myobj = gTTS(text=naam, lang=language, slow=False);
	file = str(num)+".mp3";
	myobj.save(file);
	playsound.playsound(file,True);
	os.remove(file);

def my_command(): 

	rObject = sr.Recognizer() 
	audio = '' 

	with sr.Microphone() as source: 
		print("Speak...") 
		
		# recording the audio using speech recognition 
		audio = rObject.listen(source, phrase_time_limit = 6) 
	print("Stop.") # limit 6 secs 

	try: 

		text = rObject.recognize_google(audio, language ='en-US') 
		print("You : ", text) 
		return text 

	except: 

		machine_speak("Could not understand your audio, PLease try again !") 
		return 0

def wiki(url):
	toi_article = Article(url, language="en");
	toi_article.download()
	toi_article.parse()
	toi_article.nlp()
	shubh=toi_article.text
	print(shubh);
	machine_speak(shubh);
	


def search_web(input): 

	driver = webdriver.Firefox() 
	driver.implicitly_wait(1) 
	driver.maximize_window() 

	if 'youtube' in input.lower(): 

		machine_speak("Opening in youtube") 
		indx = input.lower().split().index('youtube') 
		query = input.split()[indx + 1:]
		machine_speak("PlayList or Best video");
		hum=my_command();
		m=youtube(query);
		#print(m);
		#machine_speak("PlayList or Best video");
		#hum=my_command();
		if "best" in str(hum):
			driver.get(m);
			driver.implicitly_wait(10)
		else:
			driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query));
			driver.implicitly_wait(10)
		return

	elif 'wikipedia' in input.lower(): 

		machine_speak("Opening Wikipedia") 
		indx = input.lower().split().index('wikipedia') 
		query = input.split()[indx + 1:] 
		driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
		wiki("https://en.wikipedia.org/wiki/" + '_'.join(query));
		return

	else: 

		if 'google' in input: 

			indx = input.lower().split().index('google') 
			query = input.split()[indx + 1:] 
			driver.get("https://www.google.com/search?q=" + '+'.join(query)) 

		elif 'search' in input: 

			indx = input.lower().split().index('google') 
			query = input.split()[indx + 1:] 
			driver.get("https://www.google.com/search?q=" + '+'.join(query)) 

		else: 

			driver.get("https://www.google.com/search?q=" + '+'.join(input.split())) 

		return


# function used to open application 
# present inside the system. 
def open_application(input): 

	if "chrome" in input: 
		machine_speak("Google Chrome") 
		os.startfile('C:\\Program Files\\Google\\Chrome\\Application\\chrome') 
		return

	elif "firefox" in input or "mozilla" in input: 
		machine_speak("Opening Mozilla Firefox") 
		os.startfile('C:\\Program Files\\Mozilla Firefox\\firefox.exe') 
		return

	elif "word" in input: 
		machine_speak("Opening Microsoft Word") 
		os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\word') 
		return

	elif "excel" in input: 
		machine_speak("Opening Microsoft Excel") 
		os.startfile('C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel') 
		return

	else: 

		machine_speak("Application not available") 
		return

def mst_answer():
	app_id="Take it from the offical site of wolframalpha"
	client=wolframalpha.Client(app_id)

	while(1):
		machine_speak("Tell me your question:")
		question=my_command()
		if question==0:
			continue
		if "exit" in str(question) or "bye" in str(question):
			break
		else:
			try:
				res=client.query(question)
				ans=next(res.results).text
				machine_speak(ans)
			except:
				print("not found");





def process_text(input): 
	
		if 'search' in input or 'play' in input: 
			# a basic web crawler using selenium 
			search_web(input) 
			return

		elif "who are you" in input or "define yourself" in input: 
			speak = '''Hello, mai ek machine hoon, ek personal assistant ke jaisa jo aake Zindagi ko aashan bnaeyga, agar aap mujhe command doge
			to main aapka help karungi'''
			machine_speak(speak) 
			return

		elif "who made you" in input or "created you" in input: 
			speak = "I have been created by Shubham Madhesiya."
			machine_speak(speak) 
			return

		

		elif 'open' in input: 
			
			# another function to open 
			# different application availaible 
			open_application(input.lower()) 
			return

		elif 'web' in input: 

			machine_speak("I can search the web for you, Do you want to continue?") 
			ans = my_command() 
			if 'yes' in str(ans) or 'yeah' in str(ans): 
				search_web(input) 
			else: 
				return

		else:
			mst_answer();

			#machine_speak("Tell me your Question");
			#question=my_command()
			#app_id="3YE3PR-YY9QUAU7V2";
			#client=wolframalpha.Client(app_id);
			#res=client.query(question)
			#ans=next(res.results).text
			#machine_speak(ans)
			


		 
def project():
	while(1):
		machine_speak("What is your name?");
		name=my_command();
		if name==0:
			continue
		else:
			break

	machine_speak("Hello,"+ name +'.');
	while(1):
		machine_speak("What can i do for you:");
		answer=my_command()
		if answer==0:
			continue
		if "exit" in str(answer) or "bye" in str(answer):
			machine_speak("Ok bye, "+ name+'.');
			break
		else:
			process_text(answer);


project();
