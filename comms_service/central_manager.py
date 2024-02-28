import time
import asyncio
import contextlib

from bleak import BleakClient, BleakScanner, BleakGATTCharacteristic

async def disconnect( device ):
    await device.client.disconnect()

async def connect( device, lock ):
    device.logger.info( f"Connecting to {device.mac_address}" )
    disconnected_event = asyncio.Event()

    def disconnected_callback( client ):
        disconnected_event.set()
        device.on_disconnect_cb()

    try:
        async with contextlib.AsyncExitStack() as stack:
            device_label = ""
            async with lock:
                if device.mac_address:
                    device_label = device.mac_address
                    bleak_device = await BleakScanner.find_device_by_address( device.mac_address )
                elif device.device_name:
                    device_label = device.device_name
                    bleak_device = await BleakScanner.find_device_by_name( device.device_name )
                else:
                    device.logger.error( "Neither MAC address nor device name are set in Device" )
                    return

                if bleak_device is None:
                    device.logger.error( "Could not find device: %s", device_label )
                    return

                device.client = BleakClient( bleak_device, disconnected_callback = disconnected_callback )
                await stack.enter_async_context( device.client )
                device.logger.info( f"Connected to {device_label}" )
                stack.callback( device.logger.info, f"Disconnecting from {device_label}" )

            async def callback_handler( _, data ):
                await device.queue.put( (time.time(), data) )

            await device.client.start_notify( device.rx_characteristic, callback_handler )
            await disconnected_event.wait()
            await device.queue.put( (time.time(), None) ) # Stops the queue receiver task on disconnect

    except Exception:
        device.logger.exception( "error with %s", device.mac_address )

