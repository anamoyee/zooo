import asyncio

import nya_fmt

import zooo

from .resources import contextmanager_profiling


async def client_lp() -> None:
	fmt = nya_fmt.Formatter()

	anamoyee_id = 507642999992352779

	async with zooo.Client(
		zooo.Client.make_httpx_client("penguin-1a78-koala-98e36-seal-863117"),
	) as zcl:
		lps = await zcl.fetch_listed_profiles(anamoyee_id)

		with contextmanager_profiling():
			fmt << lps


if __name__ == "__main__":
	asyncio.run(client_lp())
