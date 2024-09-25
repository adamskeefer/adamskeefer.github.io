import speech_recognition as sr
import dictionaries as d
import re
import os
import time

word_to_int = d.word_to_int
rolls = d.roll_vars
scenes = d.scene_vars
wordss = d.int_words


def transcribe(file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file) as source:
        data = recognizer.record(source)

    try: 
        recognizer.energy_threshold = threshold
        text = recognizer.recognize_google(data)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return 1
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return 1


def build(file):
    text = transcribe(file)
    if text == 1:
        return 1
    new_name = ""
    if roll_value != -1:
        roll_num = roll_value
    else:
        if "roll" in text.lower() or "rolled" in text.lower() or "go" in text.lower():
            match = re.search(r"(roll|rolled|go) (\d|one|two|too|to|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)", text.lower())
            if match:
                roll_num = match.group(2)
                if roll_num.isalpha():
                    roll_num = word_to_int.get(roll_num)
            else:
                return 1
        else:
            return 1
    
    new_name += "R" + str(roll_num) + "_"
    
    if "scene" in text.lower() or "seen" in text.lower():
        match = re.search(r"(scene|seen) ((\d|one|two|too|to|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)+[A-Z]?)", text.lower())
        if match:
            scene_num = match.group(2)
            if scene_num.lower() in word_to_int:
                scene_num = word_to_int.get(scene_num)
            elif len(scene_num) > 1:
                if scene_num[0].isalpha():
                    scene_num[0] = word_to_int.get(scene_num[0])
                if scene_num[1].isdigit():
                    scene_num = scene_num[0] + chr(ord(scene_num[1]) - 17)
        else:
            return 1
    else:
        return 1

    new_name += "S" + str(scene_num) + "_"

    if "take" in text.lower():
        match = re.search(r"take (\d|one|two|too|to|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)", text.lower())
        if match:
            take_num = match.group(1)
            if take_num.isalpha():
                take_num = word_to_int.get(take_num)
        else:
            return 1
    else:
        return 1

    new_name += "T" + str(take_num)

    return new_name

def handleDuplicate(old, new, fileset):
    if os.path.getsize(old) == os.path.getsize(new):
        return -1
    if new not in fileset:
        fileset[new] = 1
        return 1
    else:
        current = fileset[new]
        current += 1
        fileset[new] = current
        return current 
    
def label(folder, slider_value, roll_val):
    global threshold
    global roll_value
    roll_value = roll_val
    threshold = slider_value
    print("Running...")
    start = time.time()
    fileset = {}
    renamed = 0
    total = 0
    for filename in os.listdir(folder):
        if filename.endswith(".wav"):
            total += 1
            filepath = os.path.join(folder, filename)
            new_name = build(filepath)
            if new_name == 1:
                print("Error converting file: " + filepath)
            else:   
                new_name = str(folder) + "/" + new_name
                try:
                    os.rename(str(filepath), str(new_name) + ".wav")
                    print(filepath + " renamed to " + new_name)
                    renamed += 1
                except FileNotFoundError:
                    print("File not found.")
                except PermissionError:
                    print("Permission denied.")
                except FileExistsError:
                    new_name_two = new_name + ".wav"
                    check = handleDuplicate(filepath, new_name_two, fileset)
                    if check == -1:
                        print("Duplicate File: " + new_name + " already exists")
                    else:
                        new_name = new_name + "(" + str(check) + ")" + ".wav"
                        os.rename(str(filepath), str(new_name))
                        renamed += 1
                        print(filepath + " renamed to " + new_name)
    end = time.time()
    length = end - start
    print("Successfully renamed " + str(renamed) + "/" + str(total) + " files in " + str(length) + " seconds")

