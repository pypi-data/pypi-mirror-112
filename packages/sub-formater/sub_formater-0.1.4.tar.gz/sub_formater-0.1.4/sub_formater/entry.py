import sub_formater


def main():
    assert(len(sys.argv) == 2)
    workPath = sys.argv[1]
    shows = []
    files = [f for f in os.listdir(workPath) if os.path.isfile(f)]
    for file in files:
        updateEntry = sub_formater.parseFileName(file)
        if updateEntry.file_video is None \
                and updateEntry.file_subtitle is None:
            print("unrecognized files")
            continue
        sub_formater.updateInsertVideoSubtitle(shows, updateEntry)

    for show in shows:
        print(show)
        print(show.name)
        print(show.file_video)
        print(show.file_subtitle)
        sub_formater.rename(show.file_subtitle,
                            show.file_video, workPath)
