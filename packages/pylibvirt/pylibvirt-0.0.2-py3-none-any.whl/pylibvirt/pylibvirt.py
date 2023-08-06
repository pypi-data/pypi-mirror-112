"""Main module."""
import yaml
import libvirt
from rich import print

from .modules import Network, Domain, Volume, DirStorage, DEFAULT_BUS, next_dev, get_dev
from .modules.devices import *


class Manager:
    EXCLUDE_CLASS = ['cpu', 'memory', 'boot_order', 'DiskDevice']

    def __init__(self, template: str or dict, force_redefine: bool = False):
        self.__template_path = template
        self.__force_redefine = force_redefine
        self.template = self.load_template()
        self.conn = self.connect()
        self.list_domain = []  # List of Domain
        self.list_network = []  # List of Network
        self.list_storage = []  # List of Network
        self.list_volume = []  # List of Network
        self.generate_network()
        self.generate_storage()
        self.generate_volume()
        self.generate_domain()

    def print(self):
        print(self.list_domain)
        print(self.list_network)
        print(self.list_storage)
        print(self.list_volume)

    @property
    def force_redefine(self):
        return self.__force_redefine

    @property
    def template_path(self) -> str:
        return self.__template_path

    @template_path.setter
    def template(self, template: str):
        self.__template_path = template

    @staticmethod
    def load_devices(class_name, param):
        _class = globals()[class_name]
        instance = _class(**param)
        return instance

    @staticmethod
    def target_used(domain_disks: [{}]):
        list_target_use = {}

        for disk in domain_disks:
            for name, config in disk.items():
                bus = config.get('bus', DEFAULT_BUS)
                target = config.get('target', None)
                if target:
                    l = list_target_use.get(bus, [])
                    l.append(target)
                    list_target_use.update({bus: l})
        return list_target_use

    def generate_dom_target(self, domain_disks: [{}]) -> [{}]:
        list_target_use = self.target_used(domain_disks=domain_disks)
        for disk in domain_disks:
            for name, config in disk.items():
                bus = config.get('bus', DEFAULT_BUS)
                target = config.get('target', None)
                if not target:
                    target = \
                        next_dev(dev_used=list_target_use.get(bus, []), dev=get_dev(bus=bus))[
                            0]
                    config.update({'target': target})
        return domain_disks

    def load_template(self):
        if isinstance(self.template_path, str):
            with open(self.template_path) as file:
                return yaml.safe_load(file)
        else:
            return self.template_path

    def connect(self):
        uri = self.template['provider']['uri']
        try:
            conn = libvirt.open(str(uri))
            return conn
        except libvirt.libvirtError as e:
            exit(1)

    def generate_network(self):
        networks = self.template['network'] if 'network' in self.template else []
        for network in networks:
            for name, config in network.items():
                net = Network(name=name, **config)
                if name in self.conn.listNetworks():
                    obj_net = self.conn.networkLookupByName(name)
                    self.list_network.append(obj_net)
                else:
                    self.list_network.append(self.conn.networkCreateXML(net.generate_xml()))

    def generate_storage(self):
        storages = self.template['storage'] if 'storage' in self.template else []
        for storage in storages:
            for name, config in storage.items():
                pool_type = config.pop('pool_type')
                if pool_type == 'dir':
                    dir = DirStorage(pool_name=name, **config)
                    if name in self.conn.listStoragePools():
                        self.list_storage.append(self.conn.storagePoolLookupByName(name))
                    else:
                        self.list_storage.append(self.conn.storagePoolCreateXML(dir.generate_xml()))

    def generate_volume(self):
        volumes = self.template['volume'] if 'volume' in self.template else []
        for volume in volumes:
            for name, config in volume.items():
                pool = config.pop('pool')
                clone = config.pop('clone', None)
                vol = Volume(**config)
                pool = self.conn.storagePoolLookupByName(pool)
                if config.get('name') in pool.listVolumes():
                    self.list_volume.append(pool.storageVolLookupByName(config.get('name')))
                else:
                    if not clone:
                        self.list_volume.append(pool.createXML(vol.generate_xml()))
                    else:
                        vol_to_clone = pool.storageVolLookupByName(clone)
                        self.list_volume.append(pool.createXMLFrom(vol.generate_xml(), vol_to_clone, 0))

    def generate_disk(self, domain):
        devices = list()
        disk_devices = domain['DiskDevice']
        disk_devices = self.generate_dom_target(domain_disks=disk_devices)

        for disk in disk_devices:
            for name, config in disk.items():
                pool = config.pop('pool', 'default')
                vol_name = config.pop('volume')
                pool = self.conn.storagePoolLookupByName(pool)
                volume = pool.storageVolLookupByName(vol_name)
                devices.append(DiskDevice(volume=volume, **config))
        return devices

    def generate_devices(self, domain):
        devices = []
        for device, data in domain.items():
            if device not in self.EXCLUDE_CLASS:
                for conf in data:
                    for key, value in conf.items():
                        devices.append(self.load_devices(class_name=device, param=value))
        return devices

    def create_dom(self, name, config):
        devices = []
        devices = devices + self.generate_disk(domain=config)
        devices = devices + self.generate_devices(domain=config)
        boot_order = config.get('boot_order')
        domain_type = config.get('domain_type', 'kvm')
        cpu = config.get('cpu')
        memory = config.get('memory')
        domain = Domain(name=name, devices=devices, boot_order=boot_order, domain_type=domain_type)
        domain.cpu = domain.set_cpu(**cpu)
        domain.memory = domain.set_memory(**memory)
        list_domain = [dom.name() for dom in self.conn.listAllDomains()]
        if name in list_domain:
            if self.force_redefine:
                dom = self.conn.lookupByName(name)
                dom.undefine()
                self.conn.defineXML(domain.generate_xml())
            else:
                return self.conn.lookupByName(name)
        else:
            return self.conn.defineXML(domain.generate_xml())

    def generate_domain(self):
        domains = self.template['domain'] if 'domain' in self.template else []
        for domain in domains:
            for name, config in domain.items():
                self.list_domain.append(self.create_dom(name=name, config=config))
