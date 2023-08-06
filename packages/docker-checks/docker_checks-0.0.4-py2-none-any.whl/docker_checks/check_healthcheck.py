import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkHealth():
    flag = True
    for index, line in enumerate(dockerfileContent):
            if 'healthcheck' in line.lower():
                flag = False
    if flag:
        logging.warning(' Line %s: No HEALTHCHECK directive found', index)

if __name__ == "__main__":
    checkHealth()