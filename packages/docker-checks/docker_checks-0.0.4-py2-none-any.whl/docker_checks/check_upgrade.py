import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def checkUpgradePackage():
    list = ['apt upgrade','yum upgrade']
    for index, line in enumerate(dockerfileContent):
        for keyword in list:
            if keyword in line:
                logging.warning(' Line %s: upgrade actions should be restricted as it impacts creation of immutable, consistent builds', index)

if __name__ == "__main__":
    checkUpgradePackage()