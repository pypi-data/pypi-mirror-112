from typing import Tuple


async def os_arch(hub, target_name: str, tunnel_plugin: str) -> Tuple[str, str]:
    """
    Query the system for the OS and architecture type
    """
    DELIM = "|||"
    ret = await hub.tunnel[tunnel_plugin].cmd(
        target_name, f'echo "$OSTYPE{DELIM}$MACHTYPE{DELIM}%PROCESSOR_ARCHITECTURE%"'
    )
    assert not ret.returncode, ret.stderr
    kernel, arch, winarch = ret.stdout.lower().split(DELIM, maxsplit=2)

    if "linux" in kernel:
        kernel = "linux"
        if "64" in arch:
            os_arch = "amd64"
        else:
            os_arch = "i386"
    elif "darwin" in kernel:
        kernel = "darwin"
        if "64" in arch:
            os_arch = "darwin64"
        else:
            os_arch = "darwin32"
    elif "bsd" in kernel:
        kernel = "bsd"
        if "64" in arch:
            os_arch = "amd64"
        else:
            os_arch = "i386"
    elif winarch:
        kernel = "windows"
        if "64" in winarch:
            os_arch = "win64"
        else:
            os_arch = "win32"
    else:
        raise ValueError(
            f"Could not determine arch from kernel: {kernel} arch: {arch} winarch: {winarch}"
        )
    hub.log.debug(f'Detected arch "{os_arch}" on target')
    return kernel, os_arch
