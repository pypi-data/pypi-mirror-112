import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkAddStatement():
    for index, line in enumerate(dockerfileContent):
        for keyword in list:
            if 'ADD' in line:
                logging.warning(' Line %s: Use COPY instead of ADD statement', index)

if __name__ == "__main__":
    checkAddStatement()