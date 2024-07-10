import os

class Folders:
    @staticmethod
    def create_directories():
        if not os.path.exists("./temp"):
            os.makedirs("./temp")
        
        if not os.path.exists("./temp/models"):
            os.makedirs("./temp/models")
        
        if not os.path.exists("./temp/videos"):
            os.makedirs("./temp/videos")
        
        if not os.path.exists("./temp/transcriptions"):
            os.makedirs("./temp/transcriptions")
        
        if not os.path.exists("./temp/srts"):
            os.makedirs("./temp/srts")


if __name__ == "__main__":
    CreateDirectories.create_directories()