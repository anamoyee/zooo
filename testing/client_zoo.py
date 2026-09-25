import asyncio

import nya_fmt

import zooo

from .resources import contextmanager_profiling, cookie


async def client_zoo() -> None:
	fmt = nya_fmt.Formatter()

	anamoyee_id = 507642999992352779

	async with zooo.Client(
		zooo.Client.make_httpx_client(cookie()),
	) as zcl:
		zuh = await zcl.fetch_zoo(anamoyee_id)

		with contextmanager_profiling():
			fmt << zuh


if __name__ == "__main__":
	asyncio.run(client_zoo())
