import asyncio
import logging
from device import Device

async def reader_receiver( device: Device ):
    logger.info( "Starting queue consumer for %s", device.mac_address )

    while True:
        epoch, data = await device.queue.get()

        if data is None:
            logger.info( "Got message from client about disconnection. Exiting consumer loop... for %s", device.mac_address )
            break
        else:
            logger.info( "%s %s: %r", device.mac_address, epoch, data )

async def main( logger: logging.getLogger ):
    reader_one = Device( logger = logger,
                         mac_address = "EC:89:40:D8:E0:2A" )

    reader_two = Device( logger = logger,
                         mac_address = "F2:E1:39:4E:3E:8B" )

    reader_three = Device( logger = logger,
                           mac_address = "E3:A0:A9:05:EC:45" )

    reader_one_connection_task = asyncio.create_task( reader_one.connect() )
    reader_one_receiver_task = asyncio.create_task( reader_receiver( reader_one ) )

    reader_two_connection_task = asyncio.create_task( reader_two.connect() )
    reader_two_receiver_task = asyncio.create_task( reader_receiver( reader_two ) )

    reader_three_connection_task = asyncio.create_task( reader_three.connect() )
    reader_three_receiver_task = asyncio.create_task( reader_receiver( reader_three ) )

    await asyncio.sleep( 30 )

    if reader_one.client.is_connected:
        print( f"{reader_one.mac_address} trying to disconnect" )
        await reader_one.disconnect()
    else:
        print( f"{reader_one.mac_address} is not connected" )

    await asyncio.sleep( 30 )

    if reader_two.client.is_connected:
        print( f"{reader_two.mac_address} trying to disconnect" )
        await reader_two.disconnect()
    else:
        print( f"{reader_two.mac_address} is not connected" )

    if reader_three.client.is_connected:
        print( f"{reader_three.mac_address} trying to disconnect" )
        await reader_three.disconnect()
    else:
        print( f"{reader_three.mac_address} is not connected" )

    await reader_one_connection_task
    await reader_one_receiver_task

    await reader_two_connection_task
    await reader_two_receiver_task

    await reader_three_connection_task
    await reader_three_receiver_task

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.basicConfig( level = log_level,
        format = "%(asctime)-15s %(name)-8s %(levelname)s: %(message)s" )
    logger = logging.getLogger( __name__ )
    asyncio.run( main( logger ) )
