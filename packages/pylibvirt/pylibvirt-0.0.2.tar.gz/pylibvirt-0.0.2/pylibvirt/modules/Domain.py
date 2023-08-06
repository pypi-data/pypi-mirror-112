import uuid
import string

from xml.dom import minidom

from pylibvirt.modules.devices import Device

def generate_dev(patter: str):
    alpha = string.ascii_lowercase
    l = []
    for letter in alpha:
        l.append(patter + letter)
    return l


def next_dev(dev_used: list, dev: str = 'vd'):
    dev_used = set(dev_used)
    dev_list = set(generate_dev(dev))
    return sorted(list(dev_list - dev_used))


def next_dev_from_dict(dom_xml: str, dev: str = 'vd'):
    xml = minidom.parseString(dom_xml)
    disks = xml.getElementsByTagName('disk')
    dev_used = []
    for disk in disks:
        for target in disk.getElementsByTagName('target'):
            dev_used.append(target.getAttribute('dev'))
    dev_used = set(dev_used)
    dev_list = set(generate_dev(dev))
    return sorted(list(dev_list - dev_used))


def get_dev(bus: str):
    if bus == 'scsi':
        return 'sd'
    elif bus == 'virtio':
        return 'vd'
    elif bus == 'usb':
        return 'sd'
    elif bus == 'sata':
        return 'sd'
    elif bus == 'fdc':
        return 'fd'


class Domain(Device):
    XML_NAME = "domain"

    def __init__(self, name: str, domain_type: str = "kvm", devices: list = [],
                 boot_order: list = ['network', 'cdrom', 'hd']):
        super().__init__(name=self.XML_NAME)
        self.__domain_type = domain_type
        self.__uuid = str(uuid.uuid4())
        self.__name = name
        self.__devices = devices
        self.__boot_order = boot_order
        self.__os = self.set_os()
        self.__memory = self.set_memory()
        self.__cpu = self.set_cpu()
        self.generate_data()

    @property
    def boot_order(self) -> list:
        return self.__boot_order

    @boot_order.setter
    def boot_order(self, boot_order: list):
        self.__boot_order = boot_order

    @property
    def devices(self) -> list:
        return self.__devices

    @devices.setter
    def devices(self, devices: list):
        self.__devices = devices

    @property
    def domain_type(self) -> str:
        return self.__domain_type

    @domain_type.setter
    def domain_type(self, domain_type: str):
        self.__domain_type = domain_type

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def memory(self) -> dict:
        return self.__memory

    @memory.setter
    def memory(self, memory: {}):
        self.__memory = memory
        self.generate_data()

    @staticmethod
    def set_memory(memory: int = 1, max_memory: int = 2, mem_unit: str = "G"):
        return {"memory": {
            "text": str(max_memory),
            "attr": {
                "unit": mem_unit
            }
        },
            "currentMemory": {
                "text": str(memory),
                "attr": {
                    "unit": mem_unit
                }
            }
        }

    @property
    def os(self) -> dict:
        return self.__os

    @property
    def cpu(self) -> dict:
        return self.__cpu

    @cpu.setter
    def cpu(self, cpu: {}):
        self.__cpu = cpu
        self.generate_data()

    def set_os(self, arch="x86_64", machine="q35", os_type: str = "hvm"):
        data = {
            "os": {
                "children": [{
                    "type": {
                        "attr": {
                            "arch": arch,
                            "machine": machine,
                        },
                        "text": os_type
                    }
                }]
            }
        }
        boot_section = data["os"]["children"]
        for boot in self.boot_order:
            boot_section.append({"boot": {
                "attr": {
                    "dev": boot
                }
            }})

        return data

    @staticmethod
    def set_cpu(cpu: int = 1, placement: str = 'static', cpu_model: str = 'host'):
        """
        Set the number of cpu to use in the xml
        :param cpu: Number of cpu to use
        :param placement: Values can be static or auto, default is auto
        :param cpu_model: use host to copy host configuration else choose cpu model to emulate
        :return:
        """
        data = {"vcpu": {
            "text": str(cpu),
            "attr": {
                "placement": placement
            }
        }
        }
        if cpu_model == 'host':
            data.update({"cpu": {
                "attr": {
                    "mode": "host-model",
                    "check": "partial"
                }
            }})
        else:
            data.update({"cpu": {
                "attr": {
                    "mode": "custom",
                    "match": "exact",
                    "check": "partial",
                },
                "children": {
                    "model": {
                        "text": cpu_model
                    },
                    "attr": {
                        "fallback": "allow"
                    }
                }
            }})
        return data

    def get_feature(self):
        data = {"features": {
            "children": {
                "acpi": {

                }
            }
        }
        }
        if self.domain_type == "kvm":
            data["features"]["children"].update({
                "apic": {},
                "kvm": {
                    "children": {
                        "poll-control": {
                            "attr": {
                                "state": "on"
                            }
                        }
                    }
                }
            })
        return data

    def add_device(self, device: Device):
        self.devices.append(device)

    def add_devices_to_data(self, device: Device):
        device.generate_data()
        devices = self.data[self.XML_NAME]["children"]["devices"]["children"]
        devices.append(device.data)

    def generate_data(self):
        self.data.update({
            self.XML_NAME: {
                "attr": {
                    "type": self.domain_type
                },
                "children": {
                    "name": {
                        "text": self.name
                    },
                    "uuid": {
                        "text": self.uuid
                    },
                    "devices": {
                        "children": [

                        ]
                    }
                }
            }
        })
        self.update_data(self.os)
        self.update_data(self.get_feature())
        self.update_data(self.memory)
        self.update_data(self.cpu)

        for device in self.devices:
            self.add_devices_to_data(device)
