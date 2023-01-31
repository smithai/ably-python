from ably.realtime.connection import ConnectionState
from test.ably.restsetup import RestSetup
from test.ably.utils import BaseAsyncTestCase


class TestRealtimeResume(BaseAsyncTestCase):
    async def asyncSetUp(self):
        self.test_vars = await RestSetup.get_test_vars()
        self.valid_key_format = "api:key"

    async def test_connection_resume(self):
        ably = await RestSetup.get_ably_realtime()

        await ably.connection.once_async(ConnectionState.CONNECTED)
        prev_connection_id = ably.connection.connection_manager.connection_id
        connection_key = ably.connection.connection_details.connection_key
        await ably.connection.connection_manager.transport.dispose()
        ably.connection.connection_manager.notify_state(ConnectionState.DISCONNECTED)

        await ably.connection.once_async(ConnectionState.CONNECTED)
        new_connection_id = ably.connection.connection_manager.connection_id
        assert ably.connection.connection_manager.transport.params["resume"] == connection_key
        assert prev_connection_id == new_connection_id

        await ably.close()
