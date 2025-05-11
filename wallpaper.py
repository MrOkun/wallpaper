#"resources/1.jpg"

import os
import shutil
import json
import time
import math
import glob
import sys
import subprocess
import random

import colorama

WORKING = True
G = 1

# <config.json>
UI_SCALE_COEFFICIENT = 2.4
CURRENT_WALLPAPER_INDEX = 0
DEBUG = False
WALLPAPER_PATH = ""
ALL_IMAGES = False
PREFERED_FETCH_TOOL = ""
OPACITER_PATH = ""
# </config.json>

def get_files():
    return glob.glob(WALLPAPER_PATH + "/*.png") + glob.glob(WALLPAPER_PATH + "/*.jpg") + glob.glob(WALLPAPER_PATH + "/*.jpeg") + glob.glob(WALLPAPER_PATH + "/*.mp4") + glob.glob(WALLPAPER_PATH + "/*.mkv") + glob.glob(WALLPAPER_PATH + "/*.gif")

def image_render():
    global CURRENT_WALLPAPER_INDEX
    global WALLPAPER_PATH

    lines = os.get_terminal_size().lines
    columns = os.get_terminal_size().columns

    width = round(lines * UI_SCALE_COEFFICIENT)
    height = round(width / 16 * 9)

    print("\n" * ((lines - G)))

    #os.system("clear")

    #print("test", WALLPAPER_PATH)

    #files = glob.glob(WALLPAPER_PATH + '/*.*')
    #if ALL_IMAGES:
        #files = glob.iglob("*.jpg").append(glob.iglob("*.png")).append(glob.iglob("*.jpeg"))
    #else:
        #files = glob.iglob("*.jpg")

    files = get_files()

    #print(files)

    #print(len(files))

    if (CURRENT_WALLPAPER_INDEX < 0) or (CURRENT_WALLPAPER_INDEX > len(files)):
        CURRENT_WALLPAPER_INDEX = 0

    file = files[CURRENT_WALLPAPER_INDEX]
    extension = file[file.rfind(".") + 1:]

    #print(extension)

    if (extension == "png") or (extension == "jpg") or (extension == "jpeg"):
        start = f"chafa \"{files[CURRENT_WALLPAPER_INDEX]}\" --size {width}x{height} --align center"
        os.system(start)
    elif (extension == "mp4") or (extension == "mkv") or (extension == "gif"):
        d = float(subprocess.check_output([
            "ffprobe","-v","error",
            "-show_entries","format=duration",
            "-of","default=noprint_wrappers=1:nokey=1", file
        ], stderr=subprocess.DEVNULL).strip())

        file_name = file[file.rfind("//"):]

        ts = f"{random.random() * d:.2f}"
        subprocess.run([
            "ffmpeg","-ss", ts,
            "-i", file,
            "-frames:v","1",
            "-q:v","2",
            "temp.jpg"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        start = f"chafa \"temp.jpg\" --size {width}x{height} --align center"
        os.system(start)

        os.remove("temp.jpg")
    else:
        print("script doesn't support .", extension, "files")
        sys.exit()
    #print(start)    
    #os.system(start)
    

def info_render():
    global WALLPAPER_PATH, CURRENT_WALLPAPER_INDEX, OPACITER_PATH

    files = get_files()

    #print(WALLPAPER_PATH + "/*.png")

    #i = 0
    #for file in files:
    #    print(i, file)

    info_text_file = files[CURRENT_WALLPAPER_INDEX]
    info_extension = info_text_file[info_text_file.rfind(".") + 1:]

    info_text = info_text_file[info_text_file.find("/") + 1:info_text_file.rfind(".")]

    if (info_extension == "mp4") or (info_extension == "mkv") or (info_extension == "gif"):
        info_text = info_text + "*"

    prev_info_text = "[  ]"
    next_info_text = "[  ]"

    if not(CURRENT_WALLPAPER_INDEX - 1 < 0):
        prev_text_file = files[CURRENT_WALLPAPER_INDEX - 1]
        prev_text = prev_text_file[prev_text_file.find("/") + 1:prev_text_file.rfind(".")]

        prev_info_text = f"[ {prev_text} ]"
    if not(CURRENT_WALLPAPER_INDEX + 1 > len(files) - 1):
        next_text_file = files[CURRENT_WALLPAPER_INDEX + 1]
        next_text = next_text_file[next_text_file.find("/") + 1:next_text_file.rfind(".")]

        next_info_text = f"[ {next_text} ]"

    #prev_info_text.replace("_", " ")
    #info_text.replace("_", " ")
    #next_info_text.replace("_", " ")

    width = shutil.get_terminal_size().columns

    #"q  ".rjust(round(width * 0.8))

    offset = -18

    top_body = colorama.Style.DIM + prev_info_text.center(width)[:len(prev_info_text.center(width)) + offset]
    middle_body = colorama.Style.BRIGHT + info_text.center(width)[:len(info_text.center(width)) + offset]
    bottom_body = colorama.Style.DIM + next_info_text.center(width)[:len(next_info_text.center(width)) + offset]

    top_symbol = "q  " + colorama.Style.NORMAL
    middle_symbol = "w 󰆓 " + colorama.Style.NORMAL
    bottom_symbol = "e  " + colorama.Style.NORMAL

    top = top_body + top_symbol
    middle = middle_body + middle_symbol
    bottom = bottom_body + bottom_symbol

    print(top)
    print(middle)
    print(bottom)

    print("  ".center(width)[:len("  ".center(width)) + offset] + "x 󰗽 ".ljust(width))

    print("\n" * (G))

def set_wallpaper():
    os.system("killall waybar")
    os.system("killall mpvpaper")
    os.system("killall fmmpeg")

    files = get_files()

    file = files[CURRENT_WALLPAPER_INDEX]
    extension = file[file.rfind(".") + 1:]

    if (extension == "mp4") or (extension == "mkv") or (extension == "gif"):
        d = float(subprocess.check_output([
            "ffprobe","-v","error",
            "-show_entries","format=duration",
            "-of","default=noprint_wrappers=1:nokey=1", file
        ], stderr=subprocess.DEVNULL).strip())

        file_name = file[file.rfind("//"):]

        ts = f"{random.random() * d:.2f}"
        subprocess.run([
            "ffmpeg","-ss", ts,
            "-i", file,
            "-frames:v","1",
            "-q:v","2",
            "temp.jpg"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        start = f"chafa \"temp.jpg\" --size {width}x{height} --align center"
        os.system(start)

    os.system(f"wal -i {files[CURRENT_WALLPAPER_INDEX]}")
    print(f"wal -i {files[CURRENT_WALLPAPER_INDEX]}")

    print(f"matugen image {files[CURRENT_WALLPAPER_INDEX]}")
    os.system(f"matugen image {files[CURRENT_WALLPAPER_INDEX]}")
    
    print(f"python3 {OPACITER_PATH} /home/alex/.config/waybar/colors.css")
    os.system(f"python3 {OPACITER_PATH} /home/alex/.config/waybar/colors.css")
        
    print("wal-telegram", "--wal", "-g", "-r")
    subprocess.Popen(["wal-telegram", "--wal", "-g", "-r"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    s = f'mpvpaper "*" -o "vf-add=fps=12:round=near no-audio loop fullscreen no-border video-unscaled=no vf=lavfi=[scale=w=1920:h=1080:force_original_aspect_ratio=increase,crop=1920:1080]" {files[CURRENT_WALLPAPER_INDEX]}'

    subprocess.Popen([s], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print()

    #exec-once = wal -i /home/alex/Pictures/wallpapers/vibe.png
    #exec-once = mpvpaper '*' -o "vf-add=fps=12:round=near no-audio loop fullscreen no-border video-unscaled=no vf=lavfi=[scale=w=1920:h=1080:force_original_aspect_ratio=increase,crop=1920:1080]" /home/alex/Pictures/wallpapers/vibe.png

    subprocess.Popen([f"waybar"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open("/home/alex/.config/hypr/modus_percae", "w") as f:
        f.write("exec-once = wal -R\n" + "exec-once = " + s)

    print("Ok")

    if os.path.isfile("temp.jpg"):
        os.remove("temp.jpg")

    WORKING = False

def exit():
    global WORKING

    os.system("clear")
    WORKING = False
    print("Ok")

def user_input():
    global CURRENT_WALLPAPER_INDEX

    files = get_files()

    user_input_raw = input()
    
    if user_input_raw == "q":
        if CURRENT_WALLPAPER_INDEX == 0:
            CURRENT_WALLPAPER_INDEX = len(files) - 1
        else:
            CURRENT_WALLPAPER_INDEX -= 1
    elif user_input_raw == "e":
        if CURRENT_WALLPAPER_INDEX == len(files) - 1:
            CURRENT_WALLPAPER_INDEX = 0
        else:
            CURRENT_WALLPAPER_INDEX += 1
    elif user_input_raw == "w":
        set_wallpaper()
        exit()
    elif user_input_raw == "x":
        exit()

def load_config():
    global WALLPAPER_PATH, UI_SCALE_COEFFICIENT, CURRENT_WALLPAPER_INDEX, ALL_IMAGES, DEBUG, OPACITER_PATH
    #string - yellow
    #number - blue
    #boolean - cyan
    print("Loading config...\n")

    config_text = open("config.json", "r")
    config_json = json.load(config_text)

    #wallpaper path
    wallpaper_path = config_json["wallpaper_path"]

    print("WALLPAPER_PATH = ", colorama.Fore.YELLOW, f"\"{wallpaper_path}\"", colorama.Fore.WHITE)
    WALLPAPER_PATH = wallpaper_path

    #ui scale COEFFICIENT
    ui_scale_coefficient = config_json["ui_scale_coefficient"]

    print("UI_SCALE_COEFFICIENT = ", colorama.Fore.BLUE, f"{ui_scale_coefficient}", colorama.Fore.WHITE)
    UI_SCALE_COEFFICIENT = ui_scale_coefficient

    #current wallpaper index
    current_wallpaper_index = config_json["current_wallpaper_index"]

    print("CURRENT_WALLPAPER_INDEX = ", colorama.Fore.BLUE, f"{current_wallpaper_index}", colorama.Fore.WHITE)
    CURRENT_WALLPAPER_INDEX = int(current_wallpaper_index)

    #all_images
    all_images = config_json["all_images"]

    print("ALL_IMAGES = ", colorama.Fore.BLUE, f"{all_images}", colorama.Fore.WHITE)
    ALL_IMAGES = all_images

    #debug
    debug = config_json["debug"]

    print("DEBUG = ", colorama.Fore.CYAN, f"{debug}", colorama.Fore.WHITE)
    DEBUG = debug

    #opaciter path

    opaciter_path = config_json["opaciter_path"]

    print("OPACITER_PATH = ", colorama.Fore.YELLOW, f"{opaciter_path}", colorama.Fore.WHITE)
    OPACITER_PATH = opaciter_path

    #debug
    if DEBUG:
        lines = os.get_terminal_size().lines
        columns = os.get_terminal_size().columns
        width = round(lines * UI_SCALE_COEFFICIENT)
        height = round(width / 16 * 9)

        print("\nTerminal size = ", end="")
        print(colorama.Fore.MAGENTA + f"{columns}x{lines}" + colorama.Fore.WHITE)

        print("Wallpaper size = ", end="")
        print(colorama.Fore.MAGENTA + f"{width}x{height}" + colorama.Fore.WHITE)

        print("\nWallpaper.py in", colorama.Fore.RED, "debug", colorama.Fore.WHITE, "mode.")
        print("Input", colorama.Fore.GREEN, "anything", colorama.Fore.WHITE, "to continue...")
        input()
    else:
        time.sleep(math.e / 10)

    os.system("clear")

    lines = os.get_terminal_size().lines
    columns = os.get_terminal_size().columns

    width = round(lines * UI_SCALE_COEFFICIENT)
    height = round(width / 16 * 9)

def start_fetch():
    if PREFERED_FETCH_TOOL != "":
        fetch_tools = [
            "fastfetch",
            "neofetch",
            "screenFetch",
            "archey",
            "archey3",
            "archey4",
            "pfetch",
            "ufetch",
            "hardfetch",
            "winfetch",
            "swmfetch",
            "cpufetch",
            "ferris-fetch",
            "fet.sh",
            "afetch",
            "rsfetch",
        ]

        for fetch in fetch_tools:
            if shutil.which(fetch) != None:
                os.system(fetch)
                break
    else:
        os.system(PREFERED_FETCH_TOOL)

def main():
    os.system("clear")
    load_config()
    os.system("clear")

    while WORKING:
        image_render()
        info_render()
        user_input()

    start_fetch()

if __name__ == "__main__":
    main()