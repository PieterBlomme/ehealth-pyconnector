from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from typing import Optional
import urllib.request
import subprocess
import click
import os
import tempfile
import shutil

PACKAGE_ROOT = Path(__file__).parent.parent

def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with ZipFile(zipfname, 'r') as zipread:
            with ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
                    else:
                        print(f"Removing {item.filename}")
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)

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

def generate_properties_file(path: Optional[str] = PACKAGE_ROOT):
    print("Copying be.ehealth.technicalconnector.properties")
    shutil.copy(f"{path}/java/config/be.ehealth.technicalconnector.properties", f"{path}/be.ehealth.technicalconnector.properties")
    print(f"Fixing KEYSTORE_DIR to {path}/java/config/P12/${{environment}}/")
    with open(f"{path}/be.ehealth.technicalconnector.properties") as f:
        props = f.read()
    props = props.replace("KEYSTORE_DIR=/P12/${environment}/", f"KEYSTORE_DIR={path}/java/config/P12/${{environment}}/")
    with open(f"{PACKAGE_ROOT}/be.ehealth.technicalconnector.properties", "w") as f:
        f.write(props)
        
@click.command()
@click.option('--base-path', multiple=True)
def compile_bridge(base_path):
    CLASSPATH = get_classpath()
    cmd = f"javac -cp '{CLASSPATH}' {PACKAGE_ROOT}/JavaGateway.java"
    print(cmd)
    os.system(cmd)
    generate_properties_file(base_path)

def launch_bridge():
    CLASSPATH = get_classpath()
    cmd = f"java -cp '{CLASSPATH}' {PACKAGE_ROOT}/JavaGateway.java"
    print(cmd)
    os.system(cmd)