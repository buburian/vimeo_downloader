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


| 變數 	| 說明 	| 備註 	|
|----------	|----------	|--------------------------------------------------------------------------------------------	|
| vimeo_id 	| 影片編號 	| 必須 	|
| password 	| 影片密碼 	| 如果影片需要密碼，就在這邊設定。 如果沒設定，會跳出訊息要你輸入 (公開影片這變數就不用設定) 	|
