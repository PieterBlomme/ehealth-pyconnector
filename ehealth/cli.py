from io import BytesIO
from zipfile import ZipFile
import urllib.request
import subprocess
import os

def download_packages():
    # installing the Java bridge
    DOWNLOAD_URL = "https://repo.ehealth.fgov.be/artifactory/maven2/be/fgov/ehealth/connector/connector-packaging-persphysiotherapist/4.3.0/connector-packaging-persphysiotherapist-4.3.0-java.zip"

    url = urllib.request.urlopen(DOWNLOAD_URL)

    with ZipFile(BytesIO(url.read())) as my_zip_file:
        my_zip_file.extractall('./java')

def get_classpath():
    # correctly set the Java classpath
    CLASSPATH = "./java/lib/*:./java/test-lib/*"
    ENV_PATH = subprocess.getoutput("poetry env info --path")
    PY4J_PATH = f"{ENV_PATH}/share/py4j/py4j0.10.9.7.jar"
    CLASSPATH += f":{PY4J_PATH}"
    print(f"Using Java CLASSPATH={CLASSPATH}")
    return CLASSPATH

def compile_bridge():
    CLASSPATH = get_classpath()
    cmd = f"javac -cp '{CLASSPATH}' JavaGateway.java"
    print(cmd)
    os.system(cmd)

def launch_bridge():
    CLASSPATH = get_classpath()
    cmd = f"java -cp '{CLASSPATH}' JavaGateway.java"
    print(cmd)
    os.system(cmd)