import os
import json
import base64
import http.client
from datetime import datetime


REPO = "Narutoninjawarrior/cottage-commons"
HEARTH_PATH = "hearth.json"
BRANCH = "main"


def _load_env_token():
    """
    Reads GITHUB_TOKEN from the nearest .env file without external dependencies.
    Searches from this file's directory upward to the repo root, then falls back
    to the OS environment so CI pipelines work without a .env file on disk.
    """
    search_root = os.path.dirname(os.path.abspath(__file__))
    for _ in range(3):  # walk at most 3 directories upward
        candidate = os.path.join(search_root, ".env")
        if os.path.exists(candidate):
            with open(candidate, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GITHUB_TOKEN="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        search_root = os.path.dirname(search_root)

    return os.environ.get("GITHUB_TOKEN", "")


def _read_local_hearth():
    """
    Locates and reads the local hearth.json, returning its parsed contents.
    Returns an empty memories dict if the file is missing or unreadable.
    """
    # github_api_sync.py lives in src/, hearth.json lives one level up at repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hearth_file = os.path.join(repo_root, HEARTH_PATH)

    if not os.path.exists(hearth_file):
        print(f"[GithubSync] hearth.json not found at {hearth_file} — sync skipped.")
        return None

    try:
        with open(hearth_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as err:
        print(f"[GithubSync] Could not read hearth.json: {err}")
        return None


def sync_hearth():
    """
    Pushes the local hearth.json to GitHub via the REST API (zero external dependencies).

    Workflow:
      1. Load GITHUB_TOKEN from .env (or OS environment for CI).
      2. Read the local hearth.json.
      3. Fetch the current file SHA from GitHub (required for in-place updates).
      4. PUT the updated file content back to the repository.

    Returns True on success, False on any failure — never raises.
    """
    token = _load_env_token()
    if not token:
        print("[GithubSync] GITHUB_TOKEN not found in .env or environment — sync skipped.")
        return False

    hearth_data = _read_local_hearth()
    if hearth_data is None:
        return False

    owner, repo_name = REPO.split("/", 1)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "cottage-commons-hearth-bridge",
    }

    conn = http.client.HTTPSConnection("api.github.com", timeout=30)
    try:
        # Step 1: Fetch existing file SHA so GitHub accepts the update
        conn.request("GET", f"/repos/{owner}/{repo_name}/contents/{HEARTH_PATH}", headers=headers)
        get_response = conn.getresponse()
        file_sha = None

        if get_response.status == 200:
            existing = json.loads(get_response.read().decode("utf-8"))
            file_sha = existing.get("sha")
        else:
            get_response.read()  # drain the response body

        # Step 2: Encode the hearth content for the GitHub API
        encoded_content = base64.b64encode(
            json.dumps(hearth_data, indent=4).encode("utf-8")
        ).decode("utf-8")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "message": f"[Hearth Sync] Villager1 wonder cycle complete — {timestamp}",
            "content": encoded_content,
            "branch": BRANCH,
        }
        if file_sha:
            payload["sha"] = file_sha

        # Step 3: PUT the updated file to GitHub
        conn.request(
            "PUT",
            f"/repos/{owner}/{repo_name}/contents/{HEARTH_PATH}",
            body=json.dumps(payload),
            headers=headers,
        )
        put_response = conn.getresponse()

        if put_response.status in [200, 201]:
            print(f"[GithubSync] hearth.json synced to GitHub at {timestamp}.")
            return True

        body = put_response.read().decode("utf-8")
        print(f"[GithubSync] GitHub sync failed — HTTP {put_response.status}: {body[:200]}")
        return False

    except Exception as err:
        print(f"[GithubSync] Unexpected error during sync: {err}")
        return False

    finally:
        conn.close()


def main():
    """Entry point for manual sync runs."""
    success = sync_hearth()
    if not success:
        print("[GithubSync] Sync did not complete successfully.")


if __name__ == "__main__":
    main()
