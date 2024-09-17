import speech_recognition as sr
import dictionaries as d
import re
import os
import wave

word_to_int = d.word_to_int


# def find_slate(file):
#     with wave.open(file, 'rb') as wf:
#         params = wf.getparams()
#         frames = wf.readframes(wf.getnframes())
#         chunk = 1024
#         start = 0
#         loudest = 0
#         while start < len(frames):
#             end = start + chunk
#             data = frames[start:end]
#             for sample in data:
#                 if abs(sample) > loudest:
#                     loudest = abs(sample)
#                     index = wf.tell() - len(data) + data.index(sample)
#             start += chunk
    
#     temp_path = "./temp.wav"

#     with wave.open(temp_path, 'wb') as new_wf:
#         new_wf.setparams(params)
#         data = wf.readframes(index)
#         new_wf.writeframes(data)
#     return temp_path


def transcribe(file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file) as source:
        data = recognizer.record(source)

    try: 
        recognizer.energy_threshold = 100

        text = recognizer.recognize_google(data)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def build(file):
    text = transcribe(file)
    new_name = ""
    if "roll" in text:
        match = re.search(r"roll (\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)", text)
        if match:
            roll_num = match.group(1)
            if roll_num.isalpha():
                roll_num = word_to_int.get(roll_num)
    else:
        return 1
    
    new_name += "R" + str(roll_num) + "_"
    
    if "scene" in text:
        match = re.search(r"scene (\d+[A-Z]?)", text)
        if match:
            scene_num = match.group(1)
            if len(scene_num) > 1 and scene_num[1].isdigit():
                scene_num = scene_num[0] + chr(ord(scene_num[1]) - 17)
    else:
        return 1

    new_name += "S" + str(scene_num) + "_"

    if "take" in text:
        match = re.search(r"take (\d|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)", text)
        if match:
            take_num = match.group(1)
            if take_num.isalpha():
                take_num = word_to_int.get(take_num)
    else:
        return 1

    new_name += "T" + str(take_num) + ".wav"

    return new_name

def label(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".wav"):
            filepath = os.path.join(folder, filename)
            new_name = build(filepath)
            if new_name == 1:
                print("Error converting file: " + filepath)
            else:   
                new_name = str(folder) + "/" + new_name
                try:
                    os.rename(str(filepath), str(new_name))
                    print(filepath + " renamed to " + new_name)
                except FileNotFoundError:
                    print("File not found.")
                except PermissionError:
                    print("Permission denied.")
                except FileExistsError:
                    print("Duplicate reading: " + new_name + " already exists")
