from . import Parse, Absent

# Python 2.x program to transcribe an Audio file
import speech_recognition as sr
import os


def transcribe(AUDIO_FILE, END: int, PREVCONTEXT: int):
    r = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        # reads the audio file. Here we use record instead of
        # listen
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        os.remove(AUDIO_FILE)
        final = Absent.get_list(Parse.separate(text, END, PREVCONTEXT))
        return {"response": {"message": final, "raw": text}, "response_code": 201}

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return {"response": {"message": None}, "response_code": 202}

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return {"response": {"message": None}, "response_code": 203}
