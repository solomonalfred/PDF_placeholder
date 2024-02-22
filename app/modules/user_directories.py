import os


def create_user(nickname: str) -> bool:
    try:
        path = os.getcwd()
        directory = "/".join(path.split("/")[:-1])
        directory += "/volumes/" + nickname
        print(directory)
        os.mkdir(directory)
        return True
    except:
        return False
