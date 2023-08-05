from testindata.dataset.file import File
from testindata.dataset.labeldata import LabelData
import json
import copy

class UpdateFile(File):
    def __init__(self, fdata={}, req=None, fileType="", debug=False):
        # do not edit this file, magic!!!!
        if not req:
            raise Exception(f"request for FileData must be set")

        keys = list(set(fdata.keys()))
        keys.sort()
        if keys != ['create_at', 'fid', 'fid_num', 'frame_id', 'md5', 'meta', 'name', 'path', 'ref_id', 'sensor', 'size', 'update_at', 'url']:
            raise Exception(f"bad fdata parameter, keys:{keys}")

        meta = fdata["meta"]
        if meta == []:
            meta = {}

        self.__oldData = {
            "meta": copy.copy(meta),
            "name": copy.copy(fdata["name"]),
            "frame_id": copy.copy(fdata["frame_id"]),
            "sensor": copy.copy(fdata["sensor"]),
            "ref_id": copy.copy(fdata["ref_id"])
        }

        self.__fid = fdata["fid"]
        self.__fidNum = fdata["fid_num"]
        self.referId = fdata["ref_id"]
        self.name = fdata["name"]
        self.__path = fdata["path"]
        self.__url = fdata["url"]
        self.__md5 = fdata["md5"]
        self.__size = fdata["size"]
        self.frameId = fdata["frame_id"]
        self.sensor = fdata["sensor"]
        self.metaData = meta
        self.__createAt = fdata["create_at"]
        self.__updateAt = fdata["update_at"]

        self.__list = fdata

        self.__req = req
        self.labeldata = LabelData()
        self.anotations = LabelData()

        self.TYPE_IMAGE = 0
        self.TYPE_VIDEO = 1
        self.TYPE_AUDIO = 2
        self.TYPE_POINT_CLOUD = 3
        self.TYPE_FUSION_POINT_CLOUD = 4
        self.TYPE_POINT_CLOUD_SEMANTIC_SEGMENTATION = 5
        self.TYPE_TEXT = 6

        if fileType == "":
            self.fileType = fileType
        else:
            self.fileType = self.TYPE_IMAGE

        self.debug = debug

    @property
    def path(self):
        return self.__path

    @property
    def req(self):
        return self.__req

    @property
    def fid(self):
        return self.__fid

    @property
    def fidNum(self):
        return self.__fidNum

    @property
    def url(self):
        return self.__url

    @property
    def md5(self):
        return self.__md5

    @property
    def size(self):
        return self.__size

    @property
    def createAt(self):
        return self.__createAt

    @property
    def updateAt(self):
        return self.__updateAt

    def ToList(self):
        ret = {}
        ret["file"] = self.__list
        if len(self.anotations.labels) > 0:
            ret["anotations"] = self.anotations.labels

        return ret

    def Update(self):
        self.SelfCheck()

        updateFlag = False

        updateMeta = {}
        if self.metaData != self.__oldData["meta"]:
            updateMeta = self.metaData
            updateFlag = True
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, metaData:{updateMeta}")

        updateName = ""
        if self.name != self.__oldData["name"]:
            updateName = str(self.name)
            updateFlag = True
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, name:{self.name}")

        updateFrameId = ""
        if self.frameId != self.__oldData["frame_id"]:
            updateFrameId = str(self.frameId)
            updateFlag = True
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, frameId:{self.frameId}")

        updateSensor = ""
        if self.sensor != self.__oldData["sensor"]:
            updateSensor = str(self.sensor)
            updateFlag = True
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, sensor:{self.sensor}")

        updateReferId = ""
        if self.referId != self.__oldData["ref_id"]:
            updateReferId = str(self.referId)
            updateFlag = True
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, referId:{self.referId}")

        if self.debug:
            if len(self.labeldata.labels) > 0:
                updateFlag = True
                print(f"[UPDATE_FILE] fid: {self.fid}, update label data!!")

        if not updateFlag:
            if self.debug:
                print(f"[UPDATE_FILE] fid: {self.fid}, there is nothing different from old data, abort!")
            return

        data = {
            "meta":updateMeta,
            "name":updateName,
            "frame_id":updateFrameId,
            "sensor":updateSensor,
            "anotations":self.labeldata.labels,
            "ref_id":updateReferId,
        }

        return self.req.Update(self.fid, data)

    # def GetLabels(self):
    #     info = copy.deepcopy(self.labeldata.labels)
    #     return info
    #
    # def DeleteLabels(self):
    #     self.labeldata.labels = []
    #     return True

    def Delete(self):
        return self.req.Delete(self.fid)


