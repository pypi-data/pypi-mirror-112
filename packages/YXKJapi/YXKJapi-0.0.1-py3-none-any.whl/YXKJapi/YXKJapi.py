import requests


class YXKJapi():
    def __init__(self) -> None:
        pass

    @classmethod
    def uploadFile(fileType, siteType, algorithm, path):
        mainURL = "http://172.25.17.120:8080/api/v1/upload/"
        urlParam = f"{fileType}/{siteType}/{algorithm}/"
        files = {
            "file": open(path, "rb"),
            "Content-Disposition": "form-data",
        }
        r = requests.post(mainURL+urlParam, files=files)

    @classmethod
    def donwloadFile(siteType, algorithm, fileName, savePath):  # 卫星类型、算法、文件名、保存路径
        mainURL = "http://172.25.17.120:8080/api/v1/download/"
        urlParam = f"{siteType}/{algorithm}/{fileName}"
        r = requests.get(mainURL+urlParam)
        f = open(savePath+urlParam.split("/")[-1], "wb")
        f.write(r.content)


    