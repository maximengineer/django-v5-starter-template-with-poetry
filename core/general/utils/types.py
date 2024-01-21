from pydantic import constr

hexstr = constr(pattern=r"^[0-9a-f]+$", strict=True)
