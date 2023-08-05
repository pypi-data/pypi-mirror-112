"""Declares :class:`TrustStore`."""
import asyncio

import ioc.loader

from .abstractkeystore import AbstractKeystore


class TrustStore(AbstractKeystore):
    """Like :class:`~unimatrix.ext.crypto.AbstractKeystore`, but only
    works with public keys.
    """
    __module__ = 'unimatrix.ext.crypto'

    async def load(self, loaders):
        """Loads public keys using the given `loaders`."""
        loaders = [
            ioc.loader.import_symbol(x.pop('loader'))(**x)
            for x in loaders
        ]
        await asyncio.gather(*map(self.run_loader, loaders))

    async def run_loader(self, loader):
        """Runs given `loader` and imports its keys into the
        trust store.
        """
        async for key in loader.import_keys():
            self.register(key)


trust = TrustStore()
