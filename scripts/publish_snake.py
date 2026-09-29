"""Publish only the generated SVGs; retain existing files and branch history."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

repository = os.environ["GITHUB_REPOSITORY"]
token = os.environ["GITHUB_TOKEN"]
base_url = f"https://api.github.com/repos/{repository}"


def api(path, data=None, method=None):
    request = Request(
        base_url + path,
        data=json.dumps(data).encode() if data is not None else None,
        method=method or ("POST" if data is not None else "GET"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


try:
    parent = api("/git/ref/heads/output")["object"]["sha"]
except HTTPError as error:
    if error.code != 404:
        raise
    parent = None

base_tree = api(f"/git/commits/{parent}")["tree"]["sha"] if parent else None
entries = []
for name in ("github-snake.svg", "github-snake-dark.svg"):
    content = (Path("dist") / name).read_text()
    if "<svg" not in content:
        raise ValueError(f"Expected SVG: {name}")
    entries.append({"path": name, "mode": "100644", "type": "blob", "content": content})

tree_data = {"tree": entries}
if base_tree:
    tree_data["base_tree"] = base_tree
tree = api("/git/trees", tree_data)["sha"]
if tree == base_tree:
    print("Contribution animations are already current.")
else:
    commit = api("/git/commits", {
        "message": "Refresh contribution snake animations",
        "tree": tree,
        "parents": [parent] if parent else [],
    })["sha"]
    if parent:
        api("/git/refs/heads/output", {"sha": commit, "force": False}, "PATCH")
    else:
        api("/git/refs", {"ref": "refs/heads/output", "sha": commit})
    print(f"Published both animations to output: {commit}")
