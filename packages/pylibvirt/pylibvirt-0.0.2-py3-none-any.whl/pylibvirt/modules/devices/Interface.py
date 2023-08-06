import random

from pylibvirt.modules.devices import Device


class NetworkInterfaceDevice(Device):
    XML_NAME = "interface"

    def __init__(self, net_type: str = 'network', net_interface: str = 'default',
                 model: str = 'virtio',
                 mac: str = None):
        super().__init__(name=self.XML_NAME)
        self.__net_type = net_type
        self.__net_interface = net_interface
        self.__model = model
        if not mac:
            self.mac = self.random_mac()
        else:
            self.__mac = mac
        self.generate_data()

    @staticmethod
    def random_mac():
        return "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))

    @property
    def net_type(self) -> str:
        return self.__net_type

    @net_type.setter
    def net_type(self, model: str):
        self.__net_type = model

    @property
    def mac(self) -> str:
        return self.__mac

    @mac.setter
    def mac(self, mac: str):
        self.__mac = mac

    @property
    def model(self) -> str:
        return self.__model

    @model.setter
    def model(self, model: str):
        self.__model = model

    @property
    def net_interface(self) -> str:
        return self.__net_interface

    @net_interface.setter
    def net_interface(self, net_interface: str):
        self.__net_interface = net_interface

    def generate_data(self):
        self.data.update({
            self.XML_NAME: {
                "attr": {
                    "type": self.net_type
                },
                "children": {
                    "source": {
                        "attr": {
                            self.net_type: self.net_interface
                        }
                    },
                    "mac": {
                        "attr": {
                            "address": str(self.mac)
                        }
                    },
                    "model": {
                        "attr": {
                            "type": self.model
                        }
                    }
                }
            }
        })
