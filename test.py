import asyncio
import profile

import zooo as zoo
from tcrutils.console import c
from tcrutils.string import get_token

COOKIE = get_token("COOKIE.txt")


async def test_tcr_fmt():
	c << (user := zoo.UserInfo(507642999992352779))
	c << (pid := zoo.ProfileID.KITSUNE)
	c << zoo.ProfileInfo(user=user, profile_id=pid)
	c << zoo.NPCProfileInfo.JAXPER


async def test_client_fetch_profiles_mass():
	async with zoo.Client() as zcl:
		lps = await zcl.fetch_zoo_mass(
			507642999992352779,  # $id
			309104296362901505,  # colon
			# -1,
			# 0,
			# 1,
		)

		c(lps)


async def test_client_fetch_zoo():
	async with zoo.Client(cookie=COOKIE) as zcl:
		zuh = await zcl.fetch_zoo(507642999992352779)

		c(zuh.unwrap())


async def test_client_fetch_zoo_mass():
	async with zoo.Client() as zcl:
		zuhs = await zcl.fetch_zoo_mass(
			507642999992352779,  # $id
			309104296362901505,  # colon
			-1,
			# 0,
			# 1,
		)

		c(zuhs)


async def test_client_fetch_empty():
	async with zoo.Client() as zcl:
		zuhs = await zcl.fetch_zoo_mass()

		c(zuhs)


async def main():
	# await test_tcr_fmt()
	# await test_client_fetch_zoo()
	# await test_client_fetch_profiles_mass()
	# await test_client_fetch_zoo_mass()
	await test_client_fetch_empty()


asyncio.run(main())
