import speech_recognition as sr
from gtts import gTTS
import tempfile


def speech_to_text():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand audio"

    except sr.RequestError as e:
        return f"Speech service error: {e}"


def generate_audio(text, lang):
    tts = gTTS(text=text, lang=lang)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    tts.save(temp_file.name)

    return temp_file.name