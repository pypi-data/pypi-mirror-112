import aiohttp
from typing import Any

class TWCManagerClient:
    """TWCManager client."""


    def __init__(self, host: str):
        """Construct a new TWCManager client."""
        self._host = host
    

    async def async_get_config(self) -> dict[str, Any]:
        """Get the current configuration."""
        return await self._async_get(self._host + '/api/getConfig')
    

    async def async_get_policy(self) -> dict[str, Any]:
        """Get the policy configuration."""
        return await self._async_get(self._host + '/api/getPolicy')


    async def async_get_slave_twcs(self) -> dict[str, Any]:
        """Get a list of connected slave TWCs and their state."""
        return await self._async_get(self._host + '/api/getSlaveTWCs')


    async def async_get_status(self) -> dict[str, Any]:
        """Get the current status (charge rate, policy)."""
        return await self._async_get(self._host + '/api/getStatus')
    

    async def _async_get(self,path: str,) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(path) as response:
                response.raise_for_status()
                return await response.json()
