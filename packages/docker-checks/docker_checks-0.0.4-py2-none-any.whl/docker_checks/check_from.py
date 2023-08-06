import logging
import os
dockerfileContent = open("Dockerfile", "r").readlines()

def getLineNumber(keyword):
    for index, line in enumerate(dockerfileContent):
        if keyword in line.lower():
            return index

def checkValidImage():
    index = getLineNumber('from')
    if os.popen('echo $DOCKER_CONTENT_TRUST').read() == '1':
        try:
            logs = os.popen('docker pull ' + dockerfileContent[index].split(" ")[1]).read()
        except: 
            logging.warning(' Line %s: the docker image is held in a private repository and hence can not be pulled', index)
        finally:
            if 'notary.docker.io does not have trust data' in logs:
                logging.warning(' Line %s: the docker image is not verified and hence should be used carefully', index)
    else:
        os.popen('export DOCKER_CONTENT_TRUST=1').read()
        try:
            logs = os.popen('docker pull ' + dockerfileContent[index].split(" ")[1]).read()
        except: 
            logging.warning(' Line %s: the docker image is held in a private repository and hence can not be pulled', index)
        finally:
            if 'notary.docker.io does not have trust data' in logs:
                logging.warning(' Line %s: the docker image is not verified and hence should be used carefully', index)
        os.popen('export DOCKER_CONTENT_TRUST=0').read()

def checkLatestTag():
    index = getLineNumber('from')
    if 'latest' in dockerfileContent[index].lower():
        logging.warning(' Line %s: latest keyword should not be allowed', index)
    if ':' not in dockerfileContent[index].lower():
        logging.warning(' Line %s: since no version is mentioned - docker will try to pull the latest version. Fix this by mentioning a specific version.', index)

if __name__ == "__main__":
    checkValidImage()
    checkLatestTag()