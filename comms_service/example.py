import asyncio
import logging
from device import Device

async def device_receiver( device: Device ):
    logger.info( "Starting queue consumer for %s", device.mac_address )

    while True:
        epoch, data = await device.queue.get()

        if data is None:
            logger.info( "Got message from client about disconnection. Exiting consumer loop... for %s", device.mac_address )
            break
        else:
            logger.info( "%s %s: %r", device.mac_address, epoch, data )

async def main( logger: logging.getLogger ):
    device_one = Device( logger = logger,
                         mac_address = "EC:89:40:D8:E0:2A" )

    device_two = Device( logger = logger,
                         mac_address = "F2:E1:39:4E:3E:8B" )

    device_three = Device( logger = logger,
                           mac_address = "E3:A0:A9:05:EC:45" )

    device_one_connection_task = asyncio.create_task( device_one.connect() )
    device_one_receiver_task = asyncio.create_task( device_receiver( device_one ) )

    device_two_connection_task = asyncio.create_task( device_two.connect() )
    device_two_receiver_task = asyncio.create_task( device_receiver( device_two ) )

    device_three_connection_task = asyncio.create_task( device_three.connect() )
    device_three_receiver_task = asyncio.create_task( device_receiver( device_three ) )

    await asyncio.sleep( 30 )

    if device_one.client.is_connected:
        print( f"{device_one.mac_address} trying to disconnect" )
        await device_one.disconnect()
    else:
        print( f"{device_one.mac_address} is not connected" )

    await asyncio.sleep( 30 )

    if device_two.client.is_connected:
        print( f"{device_two.mac_address} trying to disconnect" )
        await device_two.disconnect()
    else:
        print( f"{device_two.mac_address} is not connected" )

    if device_three.client.is_connected:
        print( f"{device_three.mac_address} trying to disconnect" )
        await device_three.disconnect()
    else:
        print( f"{device_three.mac_address} is not connected" )

    await device_one_connection_task
    await device_one_receiver_task

    await device_two_connection_task
    await device_two_receiver_task

    await device_three_connection_task
    await device_three_receiver_task

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.basicConfig( level = log_level,
        format = "%(asctime)-15s %(name)-8s %(levelname)s: %(message)s" )
    logger = logging.getLogger( __name__ )
    asyncio.run( main( logger ) )
