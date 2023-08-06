def checkLatestTag():
    f = open("Dockerfile", "r")
    print(f.readlines()[0])

if __name__ == "__main__":
    checkLatestTag()