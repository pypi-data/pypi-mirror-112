import os
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

from beepbeep_txflowutils.utils.utils import Utilities

class GitHubSource(Utilities):
    def __init__(self,
            root_path: str, 
            github_repo_username: str, 
            github_local_remote_name: str, 
            github_commit_comment: Mapping[str, Any] =  None,
            github_update_repo: bool = False,
            github_repo_is_org: bool = False,
            github_repo_branch: str = "main"
        ):
        self.root_path = root_path
        self.github_repo_username = github_repo_username
        self.github_local_remote_name = github_local_remote_name
        self.github_commit_comment = github_commit_comment
        self.github_repo_is_org = github_repo_is_org
        self.github_update_repo = github_update_repo
        self.github_repo_branch = github_repo_branch

    def git_push_folder(self):
        """
        Update specific local folder into a github repository username.
        Parameters:
            root_path: main root path folder of the project, 
            local_repo_name: folder name to be updated,
            github_repo_username: GitHub repo username or organisation name, 
            github_local_remote_name: GitHub repo name to update, 
            github_commit_comment (default None): string comment of the git commit,
            github_repo_is_org (default False): Whether repo name is a username or an organisation,
            github_repo_branch (default main): The name of the branch to push up
        """
        try:
            os.chdir(self.root_path)
            print("Current commit comment: ", self.github_commit_comment)
            #os.system("git init")
            #os.system(f"git remote add {github_repo_username}/{github_local_remote_name} https://github.com/{github_repo_username}/{github_local_remote_name}.git")
            #os.system(f"git add {local_repo_name} && git commit -m \"{github_commit_comment}\"")
            #os.system(f"git push -f -u {github_repo_username}/{github_local_remote_name} {github_repo_branch}")
        except FileExistsError as err:
            SystemExit(err)