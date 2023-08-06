import pkg_resources


def pre_get(hub, ctx):
    kwargs = ctx.get_arguments()
    version = kwargs.get("version")
    repo_data = kwargs.get("repo_data")
    if version:
        valid_version = pkg_resources.safe_version(version)
        assert version == valid_version, f"version {version} is not valid"

    if repo_data:
        assert version in repo_data, f"version: {version} was not found in repo_data"
