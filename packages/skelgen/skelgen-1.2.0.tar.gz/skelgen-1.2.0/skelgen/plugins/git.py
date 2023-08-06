from pathlib import Path
from collections import defaultdict
import git

class GitPlugin:
    def get_data(self, template_path: Path) -> dict:
        data = defaultdict(str)

        try:
            repo = git.Repo(template_path)
        except git.exc.InvalidGitRepositoryError:
            data["is_git_repo"] = False
            return data

        data["git_is_repo"] = True
        remote = repo.remote()
        if remote is not None:
            if len(list(remote.urls)) > 0:
                data["git_remote"] = list(remote.urls)[0]
        else:
            pass

        return data
