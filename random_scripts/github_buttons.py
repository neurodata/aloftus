#%%
# imports
import random
import json
from collections import OrderedDict

import requests
from github import Github
import pypilist

#%%
FAILED = ["RerF", "render-python", "neuroglancer-scripts"]
ON_PYPI = [
    "ndio",
    "ndmg",
    "ndparse",
    "neuroglancer",
    "rerf",
    "render-python",
    "intern",
    "ndreg",
    "neuroglancer-scripts",
]

# functions
def get_text(filename):
    r = requests.get(filename.download_url)
    return r.text


def check_pypi(package_name):
    response = requests.get(
        "https://pypi.python.org/pypi/{0}/json".format(package_name)
    )
    try:
        package_url = response.json()["info"]["package_url"]
        return True
    except ValueError:
        return False


def check_ND_pypi(repo):
    return repo.name in ON_PYPI


def get_readme(repo):
    return repo.get_contents("README.md")


def update_readme(repo, new):
    """
    updates readme with new text.
    
    Parameters
    ----------
    repo : Github repo object
        repo we care about.
    new : str
        text to append before readme.
    """
    readme = get_readme(repo)
    text = get_text(readme)
    updated = new + text
    repo.update_file(readme.path, "testing programatic github", updated, readme.sha)


def get_shield(repo):
    shield = f"![Downloads shield](https://img.shields.io/pypi/dm/{repo.name}.svg)"
    readme_txt = get_text(get_readme(repo))
    already_in = "shields.io" in readme_txt
    already_in = already_in and "Downloads shield" in readme_txt
    if check_ND_pypi(repo) and not already_in:
        return shield + "\n\n"

    return ""


# code
g = Github("loftusa", "Yvhh8fmi!")
nd = g.get_organization("neurodata")
me = nd.get_repo("aloftus")

#%%
# old

# for repo in nd.get_repos():
#     if repo.name in ON_PYPI:
#         try:
#             update_readme(repo, shield)
#             shield = get_shield(repo)
#         except:
#             print(f"repo {repo.name} failed.")
#             continue

# g = github("loftusa", "yvhh8fmi!")
# nd = g.get_organization("neurodata")
# me = nd.get_repo("aloftus")

# new = get_shield(me)
# update_readme(me, new)

#%%
# # setup and constants
g = Github("loftusa", "Yvhh8fmi!")
nd = g.get_organization("Neurodata")

# make dict with info
info = dict()
for repo in nd.get_repos():
    info[repo.name] = repo.get_clones_traffic(per="week")

# over the past 14 days
info = OrderedDict(info)

#%%
total_uniques = sum([val["uniques"] for val in info.values()])  # 270
total_clones = sum([val["count"] for val in info.values()])  # 599

# sort by total clones
sorted_clones = sorted(info.items(), key=lambda item: item[1]["count"], reverse=True)
{x[0]: x[1]["count"] for x in sorted_clones}

# sort by unique clones
# sorted(info.items(), key=lambda item: item[1]["uniques"], reverse=True)

#%%
#%%
# edit README.txt in ndmg repo
# me = nd.get_repo("aloftus")
# update_readme(me, "should be before the old text")
# README = me.get_contents("README.md")

# me.update_file(contents.path, "add downloads tag", "I can update readmes programatically", contents.sha)
# r = requests.get(README.download_url)
# r.text
#%%

# outputs

# 599 total clones in the last 14 days
# 270 unique clones in the last 14 days
