from onvif_utilities.onvif import ONVIFCamera

class Camera():
    def __init__(self,ip, port, username, password) -> None:
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.camera = ONVIFCamera(self.ip, self.port ,user=self.username, passwd=self.password, encrypt=False)
        self.media_service = self.camera.create_media_service()
        self.camera_device = self.camera.create_devicemgmt_service()