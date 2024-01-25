# **Friday - AI Voice Assistant**
```
                 ███████████            ███      █████                     
                ░░███░░░░░░█           ░░░      ░░███                      
                 ░███   █ ░  ████████  ████   ███████   ██████   █████ ████
                 ░███████   ░░███░░███░░███  ███░░███  ░░░░░███ ░░███ ░███ 
                 ░███░░░█    ░███ ░░░  ░███ ░███ ░███   ███████  ░███ ░███ 
                 ░███  ░     ░███      ░███ ░███ ░███  ███░░███  ░███ ░███ 
                 █████       █████     █████░░████████░░████████ ░░███████ 
                ░░░░░       ░░░░░     ░░░░░  ░░░░░░░░  ░░░░░░░░   ░░░░░███ 
                                                                  ███ ░███ 
                                                                 ░░██████  
                                                                  ░░░░░░ 
```

## **Video Demo** 

<video src="FRIDAY%20-%20AI%20Voice%20Assistant%20-%20CS50%20Final%20Project.mp4" controls title="Title"></video>

### https://www.youtube.com/watch?v=sJ3CxYPk1yc

## **Introduction**

**Friday** is a voice assistant developed by Aygün Servet Zurnacı as a final project for CS50X 2023. **Friday** is designed to be a versatile voice assistant with a primary focus on providing assistance for their daily routines or tasks, enabling users to access and utilize resources seamlessly while multitasking.

The program initiates its operations once the required APIs are loaded. It begins by requesting the user to say the wake word, which is **Friday**. Following this, it sets up an audio stream to capture audio input from the user. It employs a while loop to continuously listen for the wake word, utilizing the Wake Word Detection API, _pvporcupine_. That API also needs prototype files for Wake Words which can be created on _PicVoice_ website.

If the user says **_Shut down_** the program will release any previously utilized resources and proceed to shut down.

When the user says **_Friday_** the assistant is ready to accept and respond to subsequent prompts.

To enhance its functionality, **Friday** utilizes a Voice Detection API, _pvcobra_, to differentiate between speech and ambient noise. It operates within a while loop until it detects a person speaking, at which point it converts the speech into text using _Azure_'s speech-to-text capabilities. This text is then sent as a prompt to _ChatGPT_, which generates responses autonomously or calls specific functions as needed based on the provided prompt.

Once a response is generated, **Friday** employs _Azure_'s neural voice synthesis to convert the text response into speech, which is then played back to the user. The program returns to listening mode to await further user input.

Overall, **Friday** is an intelligent voice assistant that leverages various APIs and AI technologies to provide users with efficient and responsive assistance with their daily routines and tasks.


## **Features**
- **Getting prompts from user and creates responses with ChatGPT** 
- **Open Websites and Applications** - - - parameters : [_"site"_]
- **Provide Current Weather Information** - - - parameters : [_"location"_]
- **Create Files** - - - parameters : [_"filename", "extension"_]
- **Read Files** - - - parameters : [_"filename", "extension"_]



## **Contact**
For questions or assistance,

Discord - Aygun#2213

E-mail - aygun-08-zurnaci@hotmail.com
