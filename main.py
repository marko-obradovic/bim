import subprocess
from datetime import datetime


def get_branches(directory: str) -> list[str]:
    result = subprocess.run(
        ["git", "branch", "-a"],
        cwd=directory,
        capture_output=True,
        text=True,
    )

    return [branch.strip() for branch in result.stdout.splitlines()]


def get_branch_log_info(directory: str, branch: str, log_format: str) -> str:
    return subprocess.run(
        ["git", "log", "-1", f"--format=%{log_format}", branch],
        cwd=directory,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    # subprocess.run(["git", "fetch", "--all", "--prune"], capture_output=True, text=True)
    directory = "/home/kovski/Documents/repos-for-bim/tmux"
    branches = get_branches(directory)
    seen_commits = []

    for branch in branches:
        commit_hash = subprocess.run(
            ["git", "rev-parse", branch],
            cwd=directory,
            capture_output=True,
            text=True,
        ).stdout.strip()

        # If you have one of the branches locally, and it points to the same commit as the remote version, you will get a duplicate entry.
        # This prevents that and implicitly prioritises the local branch.
        if commit_hash in seen_commits:
            continue

        date = get_branch_log_info(directory, branch, "ad")

        if not date:
            continue

        formatted_date = datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z").date()

        if formatted_date.month != datetime.now().month:
            continue

        print("-------------")

        print(commit_hash)

        print(formatted_date)

        print(f"branch: {branch}")

        author = get_branch_log_info(directory, branch, "an")
        print(author)

        message = get_branch_log_info(directory, branch, "s")
        print(message)

        description = get_branch_log_info(directory, branch, "b")
        print(description)

        seen_commits.append(commit_hash)


if __name__ == "__main__":
    main()
