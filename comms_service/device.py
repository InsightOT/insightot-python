import comms_service
import logging
import asyncio
import uuid

class Device:
    rx_characteristic = uuid.UUID( '{4fcb0003-890c-46a3-ab5e-1e1f3ed3d352}' )
    tx_characteristic = uuid.UUID( '{4fcb0002-890c-46a3-ab5e-1e1f3ed3d352}' )
    msg_id = 1
    client = None

    def __init__( self,
                  logger: logging.getLogger,
                  mac_address:str = None,
                  device_name:str = None,
                  is_bluetooth:bool = True ):
        self.logger = logger
        self.mac_address = mac_address
        self.device_name = device_name
        self.is_bluetooth = is_bluetooth
        self.queue = asyncio.Queue()

    async def connect( self ):
        await comms_service.connect( self )

    def on_disconnect_cb( self ):
        self.logger.info( f"Rcvd Disconnect CB for {self.mac_address}" )

    async def disconnect( self ):
        await comms_service.disconnect( self )

    def set_bluetooth( self, is_bluetooth:bool = True ):
        self.is_bluetooth = is_bluetooth

    def set_mqtt( self, is_bluetooth:bool = False ):
        self.is_bluetooth = is_bluetooth

    async def send_command( self, command_un_slipped ):
        command = self.slip.slip_encode( bytearray( command_un_slipped ) )
        await self.client.write_gatt_char( self.tx_characteristic, command )
