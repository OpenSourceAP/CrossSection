"""
ABOUTME: Step 3 of shipping: copy the checked release folder to a Hugging Face dataset branch
ABOUTME: Refuses unless storage_checks.txt passed, the user approves, and the branch is empty

How to run (from anywhere, after 1_build.py and 2_check.py):
    python Shipping/Code/3_upload_hf.py
    Needs a Hugging Face login with write access to the org (`hf auth login`).

INPUTS:
    - Shipping/Code/ship_settings.yaml (out_gdrive, hf_repo, hf_branch, hf_private)
    - <out_gdrive>/ (the release folder) and its storage_checks.txt

OUTPUTS:
    - Hugging Face dataset <hf_repo>, branch <hf_branch>: an exact copy of
      out_gdrive (minus .DS_Store), in one commit. The repo and branch are
      created if missing; a new branch starts from the repo's (empty) initial commit. Prints a file-by-file size comparison afterwards.
"""

from pathlib import Path

from huggingface_hub import HfApi
from huggingface_hub.hf_api import RepoFile

from ship_utils import CHECKS_FILE, CHECKS_PASS_LINE, load_settings

IGNORE = ['.DS_Store', '**/.DS_Store']


def local_files(src):
    return {
        str(p.relative_to(src)): p.stat().st_size
        for p in src.rglob('*') if p.is_file() and p.name != '.DS_Store'
    }


def remote_files(api, repo, branch):
    return {
        f.path: f.size
        for f in api.list_repo_tree(repo, repo_type='dataset', revision=branch, recursive=True)
        if isinstance(f, RepoFile) and f.path != '.gitattributes'
    }


def require_checks_passed(src):
    checks = src / CHECKS_FILE
    if not checks.exists():
        raise SystemExit(f'{checks} not found. Run 2_check.py first.')
    lines = [x for x in checks.read_text().splitlines() if x.strip()]
    if not lines or lines[-1].strip() != CHECKS_PASS_LINE:
        raise SystemExit(f'{checks} does not end with "{CHECKS_PASS_LINE}". Fix the release and rerun the checks.')


def require_empty(existing, label, repo):
    if existing:
        raise SystemExit(
            f'{label} of {repo} is not empty ({len(existing)} files, e.g. {list(existing)[:5]}).\n'
            'Delete the branch by hand (or change hf_branch) and rerun.'
        )


def main(settings):
    src, repo, branch = Path(settings['out_gdrive']), settings['hf_repo'], settings['hf_branch']
    require_checks_passed(src)

    files = local_files(src)
    print(f'source:  {src}')
    print(f'target:  https://huggingface.co/datasets/{repo}/tree/{branch}')
    print(f'files:   {len(files)}, {sum(files.values()) / 1e9:.2f} GB')
    print(f'Review {src / CHECKS_FILE} before approving.')
    response = input('Upload this release to Hugging Face? [y/N]: ').strip().lower()
    if response not in ('y', 'yes'):
        raise SystemExit('Upload aborted by user.')

    api = HfApi()
    api.create_repo(repo, repo_type='dataset', private=settings['hf_private'], exist_ok=True)

    # a new branch starts from the repo's initial commit (normally just .gitattributes), not
    # main: upload_folder keeps remote files it does not overwrite, so inherited files would ship
    branches = [b.name for b in api.list_repo_refs(repo, repo_type='dataset').branches]
    if branch not in branches:
        root = api.list_repo_commits(repo, repo_type='dataset')[-1].commit_id
        require_empty(remote_files(api, repo, root), f'initial commit {root[:8]}', repo)
        api.create_branch(repo, repo_type='dataset', branch=branch, revision=root)
    require_empty(remote_files(api, repo, branch), f'branch {branch}', repo)

    print(f'Uploading {len(files)} files to {repo}@{branch} ...')
    api.upload_folder(
        repo_id=repo, repo_type='dataset', revision=branch, folder_path=src,
        ignore_patterns=IGNORE, commit_message=f'Release {branch}',
    )

    # verify names and sizes in both directions
    remote = remote_files(api, repo, branch)
    missing = sorted(set(files) - set(remote))
    extra = sorted(set(remote) - set(files))
    wrong_size = sorted(f for f in set(files) & set(remote) if files[f] != remote[f])
    for f in sorted(files):
        print(f'{files[f] / 1e6:10.1f} MB  {"ok " if remote.get(f) == files[f] else "BAD"}  {f}')
    if missing or extra or wrong_size:
        raise SystemExit(f'Verification FAILED. missing: {missing}  extra: {extra}  wrong size: {wrong_size}')
    print(f'Verified {len(files)} files on https://huggingface.co/datasets/{repo}/tree/{branch}')


if __name__ == '__main__':
    main(load_settings())
