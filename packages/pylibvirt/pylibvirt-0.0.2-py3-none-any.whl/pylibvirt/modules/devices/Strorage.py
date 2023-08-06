import libvirt
from xml.dom import minidom
from pylibvirt.modules.devices import Device

DEFAULT_BUS = 'virtio'


class DiskDevice(Device):
    XML_NAME = "disk"

    def __init__(self, volume: libvirt.virStorageVol, target: str, driver: str = 'qemu', bus: str = DEFAULT_BUS,
                 disk_type: str = "file",
                 device: str = "disk",
                 cache: str = "default", discard: str = "default",
                 detect_zeroes: str = "default", shareable: bool = False, readonly: bool = False):
        super().__init__(name=self.XML_NAME)
        self.__volume = volume
        self.__target = target
        self.__driver = driver
        self.__bus = bus
        self.__disk_type = disk_type
        self.__device = device
        self.__cache = cache
        self.__discard = discard
        self.__detect_zeroes = detect_zeroes
        self.__shareable = shareable
        self.__readonly = readonly
        self.__format = None
        self.__path = None
        self.__disk_info()
        self.generate_data()

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str):
        self.__path = path

    @property
    def format(self) -> str:
        return self.__format

    @format.setter
    def format(self, format: str):
        self.__format = format

    @property
    def driver(self) -> str:
        return self.__driver

    @driver.setter
    def driver(self, driver: str):
        self.__driver = driver

    @property
    def volume(self) -> libvirt.virStorageVol:
        return self.__volume

    @property
    def readonly(self) -> bool:
        return self.__readonly

    @readonly.setter
    def readonly(self, readonly: bool):
        self.__readonly = readonly

    @property
    def shareable(self) -> bool:
        return self.__shareable

    @shareable.setter
    def shareable(self, shareable: bool):
        self.__shareable = shareable

    @property
    def detect_zeroes(self) -> str:
        return self.__detect_zeroes

    @detect_zeroes.setter
    def detect_zeroes(self, detect_zeroes: str):
        self.__detect_zeroes = detect_zeroes

    @property
    def discard(self) -> str:
        return self.__discard

    @discard.setter
    def discard(self, discard: str):
        self.__discard = discard

    @property
    def cache(self) -> str:
        return self.__cache

    @cache.setter
    def cache(self, cache: str):
        self.__cache = cache

    @property
    def device(self) -> str:
        return self.__device

    @device.setter
    def device(self, device: str):
        self.__device = device

    @property
    def disk_type(self) -> str:
        return self.__disk_type

    @disk_type.setter
    def disk_type(self, disk_type: str):
        self.__disk_type = disk_type

    @property
    def bus(self) -> str:
        return self.__bus

    @bus.setter
    def bus(self, bus: str):
        self.__bus = bus

    @property
    def target(self) -> str:
        return self.__target

    @target.setter
    def target(self, target: str):
        self.__target = target

    def __disk_info(self):
        xml = self.volume.XMLDesc(0)
        xml = minidom.parseString(xml)
        xml_path = xml.getElementsByTagName('path')[0]
        xml_format = xml.getElementsByTagName('format')[0]
        self.path = xml_path.firstChild.data
        _format = xml_format.getAttribute('type')
        if _format == "iso":
            self.device = "cdrom"
            self.format = "raw"
            self.bus = "sata"
        else:
            self.format = _format

    def generate_data(self):
        self.data.update({
            self.XML_NAME: {
                "attr": {
                    "type": self.disk_type,
                    "device": self.device
                },
                "children": {
                    "driver": {
                        "attr": {
                            "name": self.driver,
                            "type": self.format
                        }
                    },
                    "source": {
                        "attr": {
                            "file": self.path,
                        }
                    },
                    "target": {
                        "attr": {
                            "dev": self.target,
                            "bus": self.bus
                        },
                    }
                }
            }
        })
