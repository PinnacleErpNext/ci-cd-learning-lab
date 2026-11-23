# CI/CD Learning Lab

A safe dummy Python project for learning a two-branch GitHub workflow:

- `main`: production-ready
- `develop`: integration / QA
- `feature/*`, `bugfix/*`: short-lived developer branches
- Pull Requests are the only route into `develop` and `main`.
- GitHub Actions runs linting, formatting, JSON validation, and pytest.
- QA and production workflows simulate deployments using GitHub Environments and artifacts. They do **not** connect to or modify a real server.

## 1. Create the GitHub repository

Create a repository named `ci-cd-learning-lab`.

For the easiest complete demonstration of environment approvals, make this dummy repository **public** and do not add secrets or real business data. GitHub documents that required deployment reviewers for private repositories depend on the plan; public repositories support deployment protection rules on current plans.

Initialize it with this project's files (do not select GitHub's README/license/gitignore initialization if you are uploading this complete project).

## 2. Push the initial `main` branch

```bash
git init
git add .
git commit -m "chore: initialize CI/CD learning lab"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ci-cd-learning-lab.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## 3. Create `develop`

```bash
git switch -c develop
git push -u origin develop
```

At this point both permanent branches exist.

## 4. Configure GitHub repository settings

### Default branch
Settings → General → Default branch → `develop` (optional, but convenient for this lab).

### Merge methods
Settings → General → Pull Requests:
- Allow squash merging: ON
- Allow merge commits: optional
- Allow rebase merging: optional

For this lab, use **Squash and merge** for feature PRs.

### Add branch rulesets
Settings → Rules → Rulesets → New ruleset → New branch ruleset.

Create a ruleset targeting `develop`:
- Require a pull request before merging.
- Require 1 approval.
- Dismiss stale approvals when new commits are pushed.
- Require conversation resolution.
- Require status checks to pass (select `Code Quality` after the first workflow run).
- Block force pushes.
- Restrict deletions.
- Do not allow bypassing, if available.

Create a second ruleset targeting `main` with the same rules. For `main`, also require the PR to come from `develop` as a team policy. GitHub's basic branch rules do not necessarily enforce source-branch-only PRs; enforce that through your review process or an organization-level policy/custom automation if needed.

**Important:** A one-approval rule requires an eligible reviewer other than the PR author. With only one account, test approval using a second GitHub account that has write access.

### Add GitHub Environments
Settings → Environments:
1. Create `qa`.
2. Create `production`.
3. For `production`, add yourself as a required reviewer if the repository/plan exposes that setting.
4. For this public dummy repository, no secrets are needed.

## 5. Add yourself as CODEOWNER

Edit `.github/CODEOWNERS` and replace `YOUR-GITHUB-USERNAME` with your actual username (without `@`).

The CODEOWNERS file requests your review. To make it mandatory, enable "Require review from Code Owners" in the ruleset. You need a second eligible account to approve a PR you authored.

## 6. Run the first CI check

After pushing the files, open the Actions tab. The `CI` workflow should run on the `main` and `develop` pushes.

If the check passes, return to the `develop` ruleset and require the `Code Quality` status check. Repeat for `main`.

Do not select a status check until it has appeared at least once.

## 7. Simulate a developer contribution

```bash
git switch develop
git pull origin develop
git switch -c feature/add-tax-calculator
```

Edit `src/demo_app/calculator.py` or add a small feature, then:

```bash
git add .
git commit -m "feat: add tax calculator"
git push -u origin feature/add-tax-calculator
```

On GitHub, create a PR:
- base: `develop`
- compare: `feature/add-tax-calculator`

Observe:
1. CI starts.
2. Reviewer checks the diff.
3. Reviewer requests changes or approves.
4. Merge is blocked until required checks and approvals pass.
5. Use **Squash and merge**.
6. Delete the feature branch.

The QA simulation runs after the merge to `develop`.

## 8. Simulate a production release

After QA is accepted, create a PR:
- base: `main`
- compare: `develop`

Run CI, review the PR, and merge it. The production workflow starts on the push to `main`. If the `production` environment has required reviewers configured, the job pauses for approval.

The workflow uploads a release artifact and writes a deployment summary. This is a **simulation**, not a server deployment.

## 9. Demonstrate a failed CI check

In a feature branch, intentionally add a syntax error or a failing test. Push it and open a PR. Confirm that the CI status is red and merging is blocked. Fix the issue and push again.

## 10. Important safety note

Do not add production SSH keys, ERPNext credentials, database passwords, customer data, or real server details to this lab. The deployment jobs are deliberately simulated. Actual Frappe deployment will be designed separately after this workflow is understood and tested.
