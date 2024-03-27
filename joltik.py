import requests, re, argparse, zipfile, shutil, os

MIRROR_URL = "https://mirror.unownhash.com/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Joltik")
    parser.add_argument("--arch", help="which arch to use. either arm64-v8a, or armeabi-v7a", type=str, default='arm64-v8a')
    parser.add_argument("--version", help="which version to get. specify x.xxx.x. if not provided, latest is used by default", type=str, default='latest')
    args = parser.parse_args()
    POGO_VER = None
    ARCH = args.arch
    if args.version == 'latest':
        version_index = requests.get(MIRROR_URL)
        matches = re.findall(r'com\.nianticlabs\.pokemongo_arm64-v8a_0.\d\d\d\.\d.apk', version_index.text)
        version_codes = list()
        for match in matches:
            version = re.search(r'\d\d\d.\d', match)
            version_codes.append(float(version.group()))
        version_codes.sort(reverse=True)
        POGO_VER = '0.' + str(version_codes[0])
    else:
        POGO_VER = args.version
    DOWNLOAD_URL = MIRROR_URL + f'apks/com.nianticlabs.pokemongo_{ARCH}_{POGO_VER}.apk'
    pogo_apk = requests.get(DOWNLOAD_URL)
    with open('pogo.zip', 'wb') as f:
        f.write(pogo_apk.content)
    with zipfile.ZipFile("pogo.zip","r") as z:
        z.extract(f'lib/{ARCH}/libNianticLabsPlugin.so')
    if not os.path.exists(ARCH):
        os.makedirs(ARCH)
    shutil.copyfile(f'./lib/{ARCH}/libNianticLabsPlugin.so', './' + ARCH + '/pogo.so')
    os.remove(f'./lib/{ARCH}/libNianticLabsPlugin.so')
    os.rmdir(f'./lib/{ARCH}')
    os.rmdir(f'./lib')
    os.remove(f'./pogo.zip')

    
        



    
    
