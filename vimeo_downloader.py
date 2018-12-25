import requests, re, json
import base64, os
from tqdm import tqdm
from pathlib import Path


class VimeoDownloader:
    def __init__(self):
        self.__header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate'
                        }
        self.__requests = requests.session()
        self.__config = None

    def get_title(self):
        if not self.__config:
            return None
        return self.__config['video']['title']

    def get_videourl(self):
        if not self.__config:
            return None
        # 取最高畫質
        self.__config['request']['files']['progressive'].sort(key=lambda k: int(k['quality'][0:-1]), reverse=True)
        return self.__config['request']['files']['progressive'][0]['url']

    def video(self, vimeo_id = None, password=None):
        if vimeo_id is None or vimeo_id == "":
            print("vimeo_id is required")
            return False

        req = self.__requests.get('https://www.vimeo.com/{0}/'.format(vimeo_id), headers=self.__header)
        is_private = re.search(r'class="exception_title--password iris_header">([^"]*)<\/h1>', req.text)
        if is_private and is_private.group(1) == 'This video is private':
            # 需要密碼
            if not password:
                password = input("enter password: ")
            b64passwd = base64.b64encode(password.encode("utf8")).decode("utf8")
            payload = {'password': b64passwd, 'Watch Video': ''}
            r = requests.session().post('https://player.vimeo.com/video/{0}/check-password?'
                                        'referrer=null'.format(vimeo_id), headers=self.__header, data=payload)
            config = json.loads(r.text)
            if not config:
                print("incorrect password")
                return False
            else:
                self.__config = config

        else:
            # 不需要密碼
            req = self.__requests.get('https://player.vimeo.com/video/{0}/'.format(vimeo_id), headers=self.__header)
            configObj = re.search(r'var(?:\W+)config(?:\W+)=(.*);(?:\n|\r|\n\r)?', req.text)

            if configObj:
                try:
                    config = json.loads(configObj.group(1))
                    self.__config = config
                except:
                    print("It may not be a video page")
                    return False
            else:
                print('It may not be a video page')
                return False

        return True

    def download(self, filename=None):
        if not self.__config:
            return False
        if filename:
            if os.path.dirname(filename):
                Path.mkdir(Path(os.path.dirname(filename)), parents=True, exist_ok=True)
                openfile = Path(os.path.dirname(filename)) / Path(os.path.basename(filename))
            else:
                openfile = Path(os.path.basename(filename))
        else:
            openfile = Path("%s.%s" % (self.get_title(), "mp4"))

        req = self.__requests.get(self.get_videourl(), headers=self.__header, stream=True)
        file_size = int(req.headers['Content-Length'])
        block_size = 1024
        pbar = tqdm(total=file_size, initial=0, unit='B', unit_scale=True)
        with open(openfile, "wb") as f:
            for chunk in req.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        pbar.close()


