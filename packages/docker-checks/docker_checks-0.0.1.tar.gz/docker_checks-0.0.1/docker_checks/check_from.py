def checkLatest():
    f = open("Dockerfile", "r")
    print(f.read()[0])

if __name__ == "__main__":
    checkLatest()