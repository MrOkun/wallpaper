# Wallpaper.py - wallpaper changer.

config.json uses json formatting.

__Requirements__:
1. python3 -m "pip install requirements.txt"
2. [mpvpaper](https://github.com/GhostNaN/mpvpaper)
3. [python-wal](https://github.com/dylanaraps/wal)
4. [matugen](https://github.com/InioX/matugen)
5. [wal-telegram](https://github.com/guillaumeboehm/wal-telegram)
6. ffmpeg
7. [opaciter.py](https://github.com/MrOkun/opaciter/)

__ToDO__:

- __All images search__ ("all_images" options isn't working now)
- **Save last used image index** ("current_wallpaper_index" options isn't working now)
- Add option to disable programs like matugen or stuff.

__IMPORTANT.__ "wallpaper_path" path must be full.
```
{
	"wallpaper_path": "full_path/to/wallpaper_folder",
	"ui_scale_coefficient": 2.4,
	"debug": false,
	"current_wallpaper_index": 1,
	"all_images": true
}
```

"debug" is only for developers. Actually, it displays on start configuration, configuration may change while script is running, and some devoper stuff after script start.

You must have python-wal, matugen, opaciter.py and wal-telegram then script will work right from repository, but you can remove lines that execute programs that you doesn't use.
```
os.system(f"wal -i {files[CURRENT_WALLPAPER_INDEX]}")
    print(f"wal -i {files[CURRENT_WALLPAPER_INDEX]}")

    print(f"matugen image {files[CURRENT_WALLPAPER_INDEX]}")
    os.system(f"matugen image {files[CURRENT_WALLPAPER_INDEX]}")
    
    print(f"python3 /home/alex/.config/waybar/opaciter.py /home/alex/.config/waybar/colors.css")
    os.system(f"python3 /home/alex/.config/waybar/opaciter.py /home/alex/.config/waybar/colors.css")
        
    print("wal-telegram", "--wal", "-g", "-r")
    subprocess.Popen(["wal-telegram", "--wal", "-g", "-r"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    s = f'mpvpaper "*" -o "vf-add=fps=12:round=near no-audio loop fullscreen no-border video-unscaled=no vf=lavfi=[scale=w=1920:h=1080:force_original_aspect_ratio=increase,crop=1920:1080]" {files[CURRENT_WALLPAPER_INDEX]}'
```