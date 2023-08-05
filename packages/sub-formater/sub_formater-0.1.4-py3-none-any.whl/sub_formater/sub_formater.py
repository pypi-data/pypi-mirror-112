import os
import re
import sys
from enum import Enum


class FileType(Enum):
    Unknown = 1
    Video = 5
    Video_TV = 2
    Video_Movie = 4
    Subtitle = 3
    Subtitle_TV = 6
    Subtitle_Movie = 7


class Show:
    def __init__(self, name, file_video, file_subtitle):
        self.name = name
        self.file_video = file_video
        self.file_subtitle = file_subtitle

    def __eq__(self, o):
        if type(o) is not type(self):
            return False
        return True
        # return self.name == o.name


class Episode(Show):
    def __init__(self, name, file_video, file_subtitle,
                 season_num, episode_num):
        super().__init__(name, file_video, file_subtitle)
        self.season_num = -1
        self.episode_num = -1

    def __eq__(self, o):
        if not super().__eq__(o):
            return False
        return self.season_num == o.season_num \
            and self.episode_num == o.episode_num


class Movie(Show):
    def __init__(self, name, file_video, file_subtitle):
        super().__init__(name, file_video, file_subtitle)
        return

    def __eq__(self, o):
        return super().__eq__(o)


def updateInsertVideoSubtitle(shows, entry):
    for show in shows:
        if show == entry:
            if entry.file_video is not None:
                show.file_video = entry.file_video
            if entry.file_subtitle is not None:
                show.file_subtitle = entry.file_subtitle
            return
    shows.append(entry)
    return


def parseFileName(name):
    parttern = '.*[Ss]([0-9]+)[Ee]([0-9]+).*'
    filename, ext = os.path.splitext(name)
    fileType = FileType.Unknown
    if ext == '.mkv':
        fileType = FileType.Video
    elif ext == '.ass' or ext == '.srt':
        fileType = FileType.Subtitle
    regexGroup = re.search(parttern, filename)
    if regexGroup is None:
        movie = Movie("default-movie-name", None, None)
        if fileType == FileType.Video:
            movie.file_video = name
        elif fileType == FileType.Subtitle:
            movie.file_subtitle = name
            return Movie("default-movie-name", None, name)
        return movie
    else:
        episode = Episode("default-tv-name", None, None, -1, -1)
        if fileType == FileType.Video:
            episode.file_video = name
        elif fileType == FileType.Subtitle:
            episode.file_subtitle = name
        sn, en = int(regexGroup.group(1)), int(regexGroup.group(2))
        episode.season_num, episode.episode_num = sn, en
        return episode
    return None


def rename(oldName, newName, workPath):
    if oldName is None or newName is None:
        return
    old_filename, old_ext = os.path.splitext(oldName)
    new_filename, new_ext = os.path.splitext(newName)
    new_filename_with_old_ext = new_filename + old_ext
    os.rename(os.path.join(workPath, oldName),
              os.path.join(workPath, new_filename_with_old_ext))


def main():
    assert(len(sys.argv) == 2)
    workPath = sys.argv[1]
    shows = []
    files = [f for f in os.listdir(workPath) if os.path.isfile(f)]
    for file in files:
        updateEntry = parseFileName(file)
        if updateEntry.file_video is None \
                and updateEntry.file_subtitle is None:
            print("unrecognized files")
            continue
        updateInsertVideoSubtitle(shows, updateEntry)

    for show in shows:
        print(show)
        print(show.name)
        print(show.file_video)
        print(show.file_subtitle)
        rename(show.file_subtitle, show.file_video, workPath)
