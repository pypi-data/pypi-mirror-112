import os
from typing import Any
from typing import Dict


async def read(hub, roster_file: str = "") -> Dict[str, Any]:
    """
    Read in the data from the configured rosters
    """
    ret = {}
    rend = hub.OPT.heist.renderer
    if roster_file:
        return await hub.rend.init.parse(roster_file, rend)
    for fn in os.listdir(hub.OPT.heist.roster_dir):
        full = os.path.join(hub.OPT.heist.roster_dir, fn)
        ret.update(await hub.rend.init.parse(full, rend))
    return ret
