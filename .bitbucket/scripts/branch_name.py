import os
import re

REGEX_BRANCH = r"(feature|bugfix|hotfix)[\/]*([\w]*)"

BRANCH_NAME_COMMAND = "git rev-parse --abbrev-ref HEAD"


def get_branch_name():
    """Retrieve branch name"""
    with os.popen(BRANCH_NAME_COMMAND) as stream:
        branch = stream.read().strip()

    if branch == "HEAD":
        print(
            "Branch is named 'HEAD'. This is expected in bitbucket."
            "Retrieving the branch name from github environment variables instead"
        )
        return os.environ["GITHUB_HEAD_REF"]

    print(f"Current branch is '{branch}'")

    return branch


def check_branch_name(branch):
    """Check that the branch follows the generic regex""" ""

    if re.match(REGEX_BRANCH, branch):
        print(f"The branch follows the regex '{REGEX_BRANCH}'")
        return True

    print(f"The branch '{branch}' does not follow the regex '{REGEX_BRANCH}'")
    return False


if __name__ == "__main__":
    branch = get_branch_name()
    success = check_branch_name(branch)
    if success:
        exit(0)
    exit(1)
