import os
import json
import pathlib
from datetime import datetime, timezone
import shutil


# convert unix time format to ISO format
def unixTodate(unix):
    return datetime.fromtimestamp(unix, timezone.utc).strftime("%Y%m%d_%H%M%S")


# function that does the renaming
def renamingFunction(root_dir, timestamp, title, ext):
    dupe = 1
    if os.path.exists(
        root_dir + "/" + timestamp + ext
    ):  # to take care of items taken within ms apart of one another
        while os.path.exists(root_dir + "/" + timestamp + " (" + str(dupe) + ")" + ext):
            dupe += 1

        if os.path.exists(root_dir + "/" + title):
            os.rename(
                root_dir + "/" + title,
                root_dir + "/" + timestamp + " (" + str(dupe) + ")" + ext,
            )
            tally(ext)
        else:
            return 0

        dupe = 1

    else:
        if os.path.exists(root_dir + "/" + title):
            os.rename(root_dir + "/" + title, root_dir + "/" + timestamp + ext)
            tally(ext)
        else:
            return 0
    return 1


count_jsonfiles = 0
count_jpeg = 0
count_png = 0
count_gif = 0
count_mov = 0
count_mp4 = 0
count_heic = 0
count_others = 0


def tally(ext):
    global count_jsonfiles
    global count_jpeg
    global count_png
    global count_gif
    global count_mov
    global count_mp4
    global count_heic
    global count_others

    if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
        count_jpeg += 1
    elif ext.lower() == ".png":
        count_png += 1
    elif ext.lower() == ".gif":
        count_gif += 1
    elif ext.lower() == ".mov":
        count_mov += 1
    elif ext.lower() == ".mp4":
        count_mp4 += 1
    elif ext.lower() == ".heic":
        count_heic += 1
    elif ext.lower() == ".json":
        0
    else:
        count_others += 1


if __name__ == "__main__":
    # ask for folder path
    root_dir = input("Enter the path of the folder where the photos are stored: ")
    root_dir = root_dir.strip("'")
    meta_folder = root_dir + "/metadata"

    # check if metadata has been moved alr
    if os.path.exists(meta_folder):
        print("exists")

    else:
        os.makedirs(meta_folder)

        for path in pathlib.Path(root_dir).iterdir():
            fileName, fileExtension = os.path.splitext(path)
            if fileExtension == ".json":
                count_jsonfiles += 1
                shutil.move(path, meta_folder)

    # iterate through every json file, rename accordingly
    for meta in pathlib.Path(meta_folder).iterdir():
        f = open(meta)
        data = json.load(f)
        try:
            timestamp = unixTodate(int(data["photoTakenTime"]["timestamp"]))
        except:
            continue
        if (
            meta.name[:-5][-1:] == ")"
        ):  # for names like lp_image.heic(32).json and IMG_5881.HEIC(1).json
            n = meta.name[:-5][:-1].split("(")[1]
            title = (
                meta.name.split(".")[0]
                + "("
                + n
                + ")"
                + "."
                + meta.name.split(".")[1].split("(")[0]
            )
        else:
            title = data["title"]

        if (
            title[:8] == "lp_image" or title[:4] == "IMG_"
        ):  # these two file names tend to have a .MP4 file along with the original image file because theyre live photos
            ext = "." + title.split(".")[1]
            renamingFunction(root_dir, timestamp, title, ext)
            title = title.split(".")[0] + ".MP4"
            ext = ".MP4"
        else:
            ext = "." + title.split(".")[1]

        if renamingFunction(root_dir, timestamp, title, ext) == 0:
            # try the same title but with MP4 extension again
            try:
                title = title.split(".")[0] + ".MP4"
                ext = ".MP4"
                renamingFunction(root_dir, timestamp, title, ext)

            except:
                print("not found", title)

        # rename JSONs
        ext = ".json"
        renamingFunction(meta_folder, timestamp, meta.name, ext)

        f.close()

    print("JSON files:", count_jsonfiles)
    print("MOV files:", count_mov)
    print("MP4 files:", count_mp4)
    print("GIF files:", count_gif)
    print("JPEG files:", count_jpeg)
    print("PNG files:", count_png)
    print("HEIC files:", count_heic)
    print("Other files:", count_others)
    print(
        "\nTotal media:",
        count_others
        + count_gif
        + count_png
        + count_jpeg
        + count_gif
        + count_mp4
        + count_mov
        + count_heic,
    )
