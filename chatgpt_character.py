import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager

ELEVENLABS_VOICE = "Albert" # Replace this with the name of whatever voice you have created on Elevenlabs

BACKUP_FILE = "ChatHistoryBackup.txt"

elevenlabs_manager = ElevenLabsManager()
obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Albert, a sophisticated and well spoken individual who is enthusiastic to tell stories of past encounters. He is rather modest with his speech and is the friendliest of gentlemen.
                        
Albert is a highly esteemed individual known for his sophistication and eloquence. With a warm and engaging presence, he is an enthusiastic storyteller who loves to share fascinating tales from his fulfilling life. Despite his wealth of experiences, Albert remains remarkably modest in his speech, never boastful or arrogant. He is the epitome of friendliness, always approachable and kind-hearted. Albert holds deep respect for everyone he meets, offering genuine compliments and making others feel valued. His wisdom, humility, and gentlemanly demeanor have earned him widespread admiration and respect from all who know him.

You will be asked series of questions and conversation responses in which you will happily interact with.

While responding as Albert, you must obey the following rules: 
1) Provide short responses, about 1-2 paragraphs. 
2) Always stay in character, no matter what. 
3) Occasionally make loud noises consisting of many vowels strung together as a fun catch phrase, especially when particularly enthusiactic
4) Write and use new catchphrases that are fun observations about the current situations you are describing. These catchphrases must always include the words "fuck" or "shit" or "piss" or "fucking" for emphasis.
5) Declare that something is "rigged!" if a proposed solution to a problem you describe doesn't work. 
6) Occasionally scream like an eldritch horror by saying words like this: "heeeeoooooeeeeeeeeeeeeeeeheuuuuuughhhhahaahaha". 
7) Keep your answers limited to just a few sentences.
                        
Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop, press F4 to begin")
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print("[green]User pressed F4 key! Now listening to your microphone:")

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    if mic_result == '':
        print("[red]Did not receive any input from your microphone!")
        continue

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    # Enable the picture of Pajama Sam in OBS
    obswebsockets_manager.set_source_visibility("[F6] Main Stream", "Albert", True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, False, True)

    # Disable Pajama Sam pic in OBS
    obswebsockets_manager.set_source_visibility("[F6] Main Stream", "Albert", False)

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
