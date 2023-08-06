def __init__(hub):
    hub.artifact.ACCT = ["artifact"]


def get(hub):
    # TODO Determine which artifact to use, find the right plugin, and execute it's get function
    ...


def version(hub):
    # TODO Determine which artifact to use, find the right plugin, and find out the target's version of the artifact
    ...


def deploy(hub):
    # TODO Determine which artifact to use, find the right plugin, and execute it's deploy function
    ...


async def clean(hub, target_name, tunnel_plugin):
    """
    Clean up the deployed artifact and files
    """
    # remove run directory
    run_dir = hub.heist.CONS[target_name]["run_dir"]
    ret = await hub.tunnel[tunnel_plugin].cmd(target_name, f"[ -d {run_dir} ]")
    if ret.returncode == 0:
        await hub.tunnel[tunnel_plugin].cmd(target_name, f"rm -rf {run_dir}")

    # remove parent directory if its empty
    # If its not empty, there might be another running instance of heist that
    # was previously deployed
    await hub.tunnel[tunnel_plugin].cmd(
        target_name, f"rmdir {hub.heist.CONS[target_name]['run_dir'].parent}"
    )
