import openai
import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

# Initialize the recognizer
listener = sr.Recognizer()

# Set your OpenAI API key
openai.api_key = "your Api key"

# Main loop
while True:
    try:
        with sr.Microphone() as source:
            print("Speak now...")
            voice = listener.listen(source)
            data = listener.recognize_google(voice)
            print("You said:", data)

        if "exit" in data.lower():
            print("Exiting...")
            break

        # Send prompt to OpenAI Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4"
            messages=[
                {"role": "user", "content": data}
            ],
            max_tokens=1024,
            temperature=0.5
        )

        # Get the response text
        answer = response['choices'][0]['message']['content'].strip()

        # Choose output method
        choice = int(input("Press 1 to print the response or 2 to print and hear the response: "))

        if choice == 1:
            print("ChatGPT:", answer)
        else:
            print("ChatGPT:", answer)
            engine.say(answer)
            engine.runAndWait()

        # Ask whether to repeat
        repeat = input("Do you want to ask more questions? (yes/no): ")
        if repeat.lower() == "no":
            print("Goodbye!")
            break

    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except Exception as e:
        print("An error occurred:", str(e))
