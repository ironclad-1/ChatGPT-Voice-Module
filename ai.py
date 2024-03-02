import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "sk-n8DdroZiX2pBoecjXoTnT3BlbkFJQrRyEbr5ND2Z5bKfsX"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the recognizer
recognizer = sr.Recognizer()

def transcribe_audio_to_text(filename):
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_sphinx(audio)  # Use Sphinx for audio recognition
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for the user to say "genius"
        print("Say 'Hello' to start recording your question....")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)  # Use Sphinx for the trigger phrase
                if transcription.lower() == "hello":
                    # Record audio
                    filename = "input.wav"
                    print("Say your Question...")
                    with sr.Microphone() as source:
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        # Generate response using GPT-3
                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        # Read response using text-to-speech
                        speak_text(response)
            except Exception as e:
                print("An Error occurred: {}".format(e))

if __name__ == "__main__":
    main()
