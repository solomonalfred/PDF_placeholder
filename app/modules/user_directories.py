import os


def create_user(nickname: str) -> bool:
    path = os.getcwd()
    directory = "/".join(path.split("/")[:-1])
    directory += "/" + nickname
    os.mkdir(directory)
    return True
