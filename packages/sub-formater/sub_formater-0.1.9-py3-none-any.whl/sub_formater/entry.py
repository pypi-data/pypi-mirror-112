import sys
import os
import subprocess
from sub_formater import sft


def main():
    assert(len(sys.argv) == 2)
    workPath = sys.argv[1]
    shows = []
    files = [f for f in os.listdir(workPath) if os.path.isfile(f)]
    for file in files:
        updateEntry = sft.parseFileName(file)
        if updateEntry.file_video is None \
                and updateEntry.file_subtitle is None:
            print("unrecognized files")
            continue
        sft.updateInsertVideoSubtitle(shows, updateEntry)

    for show in shows:
        print(show)
        print(show.name)
        print(show.file_video)
        print(show.file_subtitle)
        if show.file_video is None or show.file_subtitle is None:
            return
        show.file_subtitle = sft.rename(show.file_subtitle,
                                        show.file_video, workPath)
        subprocess.run(["ffs", show.file_video, "-i", show.file_subtitle, "-o", show.file_subtitle],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
