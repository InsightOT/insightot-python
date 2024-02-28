import central_manager
import mqtt_manager
import asyncio

bluetooth_callback = None
mqtt_callback = None
lock = asyncio.Lock()

async def connect( device ):
    if device.is_bluetooth:
        await central_manager.connect( device, lock )
    else:
        device.logger.error( "Connect MQTT not implemented" )

async def disconnect( device ):
    if device.is_bluetooth:
        await central_manager.disconnect( device )
    else:
        device.logger.error( "Disconnect MQTT not implemented" )
