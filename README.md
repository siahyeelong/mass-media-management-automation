# Mass media management automation

The purpose of this project was to name my photos and videos downloaded from Google Photos using the Takeout function. The main.py script simply sorts all json files into a folder and renames all photos and videos according to the timestamp saved in its corresponding metadata.

# Usage
## Downloading photos from takeout
From takeout.google.com, select Google Photos and request for a takeout of all your google photos. It will take a while depending on how many photos and videos you store, but eventually the link for the download should be sent to your email. Download your media from the link provided

## Locating the folder
Locate your photos in the Downloads folder. Copy the path of the folder.

## Run the main script
In the terminal, run 
```bash 
python main.py
``` 
As prompted, paste the path of the folder you just copied. At this point, the script will rename the media and sort all json files into the `metadata` folder
