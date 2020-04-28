import os

class App:
    name = 'PuzzleHack'
    description = 'Puzzle building tools with computer vision'
    version = 'v0.1'

class Path:
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA = os.path.join(BASE, 'data')

    @classmethod
    def listall(cls, dirpath, condition=None, fullpath=False):
        all_files = os.listdir(dirpath)
        list_ = []
        
        if condition is None: return all_files

        for file_ in all_files:
            path = os.path.join(dirpath,file_)
            if condition(path):
                list_.append(path) if fullpath else list_.append(file_)

        return list_

    @classmethod
    def listdirs(cls, dirpath, fullpath=False):
        return cls.listall(dirpath=dirpath,condition=os.path.isdir,fullpath=fullpath)

    @classmethod
    def listfiles(cls, dirpath, filter_=[], fullpath=False):
        filelist = cls.listall(dirpath=dirpath,condition=os.path.isfile,fullpath=fullpath)
        if len(filter_)!=0:
            filelist = [file for file in filelist if file.split('.')[-1] in filter_]
        
        return filelist