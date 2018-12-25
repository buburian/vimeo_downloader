# vimeo_downloader
vimeo_downloader

下載vimeo需要密碼的影片或是公開影片
(當然要知道密碼)



#### 基本使用
    v = VimeoDownloader()
    ret = v.video(vimeo_id="VIMEOID", password="PASSWORD")
    # 回傳 False 代表沒抓到影片資料
    if ret:
        print("video title is: {0}".format(v.get_title())) # 獲得影片標題
        print("video url is: {0}".format(v.get_videourl())) # 獲得影片連結
        v.download() # 使用影片標題當檔名下載
        v.download("tmp/video.mp4") # 下載影片到tmp下存成video.mp4
    