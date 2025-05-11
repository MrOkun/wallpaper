# Wallpaper.py - wallpaper changer.

config.json uses json formatting.
 

ToDO:

- __All images search__ ("all_images" options isn't working now)
- **Save last used image index** ("current_wallpaper_index" options isn't working now)

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