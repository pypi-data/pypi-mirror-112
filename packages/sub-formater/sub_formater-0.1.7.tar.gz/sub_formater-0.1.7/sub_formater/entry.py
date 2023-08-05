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
        sft.rename(show.file_subtitle,
                   show.file_video, workPath)
