import json
import os

import aiofiles


async def dump(data, name="out", outdir="./var"):
    path = os.path.join(outdir, f"{name}.json")
    async with aiofiles.open(path, mode="w") as f:
        await f.write(json.dumps(data, indent=2))


def insert(obj, item, idx=0):
    obj.insert(idx, item)
    return obj
