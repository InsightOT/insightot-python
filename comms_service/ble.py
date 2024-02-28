import bleak
import platform
import asyncio

def device_sort(device):
    return device.address

class Central_Manager:
    client = None
    # nu_lookup = {'prov-session': 'ff51', 'prov-config': 'ff52', 'proto-ver': 'ff53'}
    # srv_uuid_fallback = '021a9004-0382-4aea-bff4-6b3f1c5adfb4'

    def __init__(self):
        pass

    async def bleak_connect(self, devname, chrc_names, fallback_srv_uuid, mac_address):
        self.devname = devname
        self.srv_uuid_fallback = fallback_srv_uuid
        self.chrc_names = [name.lower() for name in chrc_names]
        self.advertisement_data = None

        print('Discovering...')
        try:
            devices = await bleak.BleakScanner.discover()
        except bleak.exc.BleakDBusError as e:
            if str(e) == '[org.bluez.Error.NotReady] Resource Not Ready':
                raise RuntimeError('Bluetooth is not ready. Maybe try `bluetoothctl power on`?')
            raise

        found_device = None
        loops = 0

        if self.devname is None:
            while True:
                if len(devices) == 0:
                    print('No devices found!')
                    return False

                devices.sort(key=device_sort)=
                for i, _ in enumerate(devices):
                    if (devices[i].address == mac_address):
                        self.devname = devices[i].name
                        found_device = devices[i]
                        break

                if loops > 10:
                    print('No devices found after loops')
                    return False

                loops += 1
                devices = await bleak.BleakScanner.discover()

        else:
            for d in devices:
                if d.name == self.devname:
                    found_device = d

        if not found_device:
            raise RuntimeError('Device not found')

        print('Connecting...')
        self.device = bleak.BleakClient(found_device.address)
        await self.device.connect()

        if platform.system() == 'Windows':
            await self.device.pair()

        return True

    def get_services(self):
        print('Getting Services...')
        services = await self.device.get_services()

        service = services[self.srv_uuid_adv] or services[self.srv_uuid_fallback]
        if not service:
            await self.device.disconnect()
            self.device = None
            raise RuntimeError('Provisioning service not found')

        nu_lookup = dict()
        for characteristic in service.characteristics:
            for descriptor in characteristic.descriptors:
                if descriptor.uuid[4:8] != '2901':
                    continue
                readval = await self.device.read_gatt_descriptor(descriptor.handle)
                found_name = ''.join(chr(b) for b in readval).lower()
                nu_lookup[found_name] = characteristic.uuid
                self.characteristics[characteristic.uuid] = characteristic

        match_found = True
        for name in self.chrc_names:
            if name not in nu_lookup:
                # Endpoint name not present
                match_found = False
                break

        # Create lookup table only if all endpoint names found
        self.nu_lookup = [None, nu_lookup][match_found]

        return True

nu_lookup = {'prov-session': 'ff51', 'prov-config': 'ff52', 'proto-ver': 'ff53'}
service_uuid = '021a9004-0382-4aea-bff4-6b3f1c5adfb4'

ble = Central_Manager()
asyncio.run( ble.bleak_connect( None, nu_lookup.keys(), service_uuid, "7C:DF:A1:BC:4B:4E" ) )
