import os


def cookie() -> str:
	"""Get the cookie from the environment variable 'ZOOO_COOKIE'. If the environment variable is not set, raise RuntimeError."""
	cookie = os.environ.get("ZOOO_COOKIE", None)

	if cookie is not None:
		return cookie

	msg = "ZOOO_COOKIE environment variable is unset, use the tools/run_testing.sh script to set it up automatically from a password manager."
	raise RuntimeError(msg)
