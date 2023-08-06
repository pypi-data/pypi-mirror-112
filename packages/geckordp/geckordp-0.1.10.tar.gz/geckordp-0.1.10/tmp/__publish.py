import os
import shutil
import argparse
from pathlib import Path
from getpass import getpass
import subprocess
import keyring


def execute_process(cmd):
    popen = subprocess.Popen(
        cmd, universal_newlines=True, shell=False)
    _return_code = popen.wait()


def main():
    """ # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--public", action="store_true",
                        help="Publish package on non-test pypi")
    args, _ = parser.parse_known_args()

    # set parameters
    wallet = "kdewallet"
    service = "system"
    token_name = "test_pypi"
    pypi_url = "testpypi"
    if (args.public):
        pypi_url = "pypi"
        token_name = "pypi_api"

    # get token if available
    out = subprocess.run([
        "kwallet-query",
        "-f",
        service,
        "-r",
        token_name,
        wallet, ],
        shell=False,
        capture_output=True)
    token = out.stdout.decode("utf-8").replace("\n", "")
    if ("Failed" in token):
        token = ""

    # if not available set token
    if (token == ""):
        print(
            f"no token was found for '{token_name}', please enter your API token:")
        token = getpass("Token: ")
        token = token.replace("\n", "")
        keyring.set_password(service, token_name, token)

    # build package
    dist = Path(".").absolute().joinpath("dist")
    if (dist.exists()):
        shutil.rmtree(dist)
    execute_process([
        "python",
        "setup.py",
        "sdist",
    ]) """

    # build documentation
    docs = Path(".").absolute().joinpath("docs")
    if (not docs.exists()):
        #shutil.rmtree(docs)
        os.mkdir(str(docs))
    
    shutil.copyfile("README.md", "geckordp/index.md")


    """ execute_process([
        "sphinx-apidoc",
        "-o",
        str(Path().absolute()),
        "geckordp"
    ]) """

    execute_process([
        "sphinx-build",
        "-b",
        "html",
        "geckordp",
        "docs"
    ])

    os.remove("geckordp/index.md")


    return




    # upload package
    execute_process([
        "twine",
        "upload",
        "--repository",
        pypi_url,
        "-u",
        "__token__",
        "-p",
        token,
        str(Path(".").absolute().joinpath("dist").joinpath("*")),
    ])


if __name__ == "__main__":
    main()
