import subprocess
from datetime import datetime


def display_info(
    branch: str, commit_hash: str, formatted_date: str, directory: str
) -> None:
    print(f"\nBranch: {branch}")
    # Print the length of the above print statmement so that the underline is dynamic
    print("─" * (8 + len(branch)))

    print(f"\n{commit_hash}\n")
    print(formatted_date)

    author = get_branch_log_info(directory, branch, "an")
    print(author)

    message = get_branch_log_info(directory, branch, "s")
    print(message)

    description = get_branch_log_info(directory, branch, "b")
    print(description)


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
    # directory = "/home/kovski/Documents/repos-for-bim/tmux"
    directory = "/home/kovski/Documents/git-testing/"

    branches = get_branches(directory)
    seen_commits = []
    remote_head = subprocess.run(
        ["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"],
        cwd=directory,
        capture_output=True,
        text=True,
    ).stdout.strip()

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

        # if formatted_date.month != datetime.now().month:
        #     continue

        seen_commits.append(commit_hash)

        parent_commit_hash = subprocess.run(
            ["git", "rev-parse", f"{branch}^"],
            cwd=directory,
            capture_output=True,
            text=True,
        ).stdout.strip()

        print(f"Parent commit: {parent_commit_hash}")

        while parent_commit_hash:
            parent_commit_hash = subprocess.run(
                ["git", "rev-parse", f"{parent_commit_hash}^"],
                cwd=directory,
                capture_output=True,
                text=True,
            ).stdout.strip()

            print(f"Parent commit: {parent_commit_hash}")

            branch_name = subprocess.run(
                ["git", "branch", "-a", "--contains", f"{parent_commit_hash}"],
                cwd=directory,
                capture_output=True,
                text=True,
            ).stdout.strip()

            print(f"branch name: {branch_name}")

        # display_info(branch, commit_hash, formatted_date, directory)

    print(remote_head)


if __name__ == "__main__":
    main()
