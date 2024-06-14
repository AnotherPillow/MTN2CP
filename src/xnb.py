import os, urllib.request, shutil
from .Logger import logger

def downloadXNBCLI():
    if os.name == "nt":
        #check if x64 or x86
        if sys.maxsize > 2**32:
            url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-windows-x64.zip"
        else:
            url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-windows-x86.zip"
    elif os.name == "posix":
        url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-macos.zip"
    else:
        url = "https://github.com/LeonBlade/xnbcli/releases/download/v1.0.7/xnbcli-linux.zip"

    if not os.path.exists('xnbcli'):
        os.mkdir('xnbcli')
        logger.info('Downloading xnbcli')
        urllib.request.urlretrieve(url, "xnbcli/xnbcli.zip")
    else:
        logger.info('xnbcli already downloaded, skipping download.')
    

    if os.path.exists('xnbcli/xnbcli.zip'):
        logger.info('Unpacking xnbcli')
        shutil.unpack_archive("xnbcli/xnbcli.zip", "xnbcli/bin")
    else:
        return

def chmodIfNeeded(file):
    if os.name =='nt': return
    os.system(f'chmod +x "{file}"')

def _getXnbExecutable():
    if os.name == 'nt': 
        return 'xnbcli/bin/xnbcli.exe'
    return 'xnbcli/bin/xnbcli'

xnbcliExecutable = _getXnbExecutable()

def extractFilesInADirectory(dir = 'input'):
    cmd = f'"{xnbcliExecutable}" unpack "{dir}" "{dir}"'
    os.system(cmd)
