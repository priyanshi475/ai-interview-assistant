import pyttsx3
import speech_recognition as sr
import time

def speak(text):
    engine = pyttsx3.init()
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting noise... please wait")
        r.adjust_for_ambient_noise(source, duration=2)

        print("Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        text = r.recognize_google(audio, language="en-IN")
        print("You said:", text)
        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand clearly")
        return ""

    except sr.RequestError:
        print("Internet issue")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

def give_feedback(answer):
    if answer == "":
        return "I could not understand your answer.", 0
    elif "don't know" in answer or "no idea" in answer:
        return "You should prepare this question.", 1
    elif len(answer.split()) < 5:
        return "Try to explain more.", 2
    else:
        return "Good answer.", 3

questions = [
    "Tell me about yourself",
    "What are your strengths",
    "Why should we hire you"
]

answers = []
scores = []

speak("Interview is starting")

for i, q in enumerate(questions):
    speak(f"Question {i+1}")
    speak(q)

    ans = listen()
    answers.append(ans)

    feedback, score = give_feedback(ans)
    scores.append(score)

    speak("Your answer is noted")
    speak(feedback)

speak("Interview finished. Here is your overall feedback")

total = sum(scores)

if total <= 3:
    speak("You need improvement")
elif total <= 6:
    speak("Your performance is average")
else:
    speak("Great job")

print("\n--- INTERVIEW SUMMARY ---")
for i, q in enumerate(questions):
    print(f"Q{i+1}: {q}")
    print(f"Your Answer: {answers[i]}")
    print()

print("Total Score:", total)