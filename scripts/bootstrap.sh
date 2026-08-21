#!/usr/bin/env bash
#
# Prepare this repository for its first push to GitHub.
#
#   ./scripts/bootstrap.sh <github-user-or-org> [repo-name]
#
# Replaces the OWNER placeholders throughout, initialises git if needed, and
# makes the first commit. It does not push -- that stays your decision.

set -euo pipefail

OWNER="${1:-}"
REPO="${2:-ai-computing-encyclopedia}"

if [[ -z "$OWNER" ]]; then
  echo "usage: $0 <github-user-or-org> [repo-name]" >&2
  exit 1
fi

cd "$(dirname "$0")/.."

echo "→ Rewriting placeholders to ${OWNER}/${REPO}"
FILES=$(grep -rl --exclude-dir=.git --exclude-dir=build --exclude-dir=site \
  --exclude-dir=.venv -e 'OWNER' -e 'ai-computing-encyclopedia' . || true)

for file in $FILES; do
  sed -i.bak \
    -e "s|Iamhifza/encyclopedia|${OWNER}/${REPO}|g" \
    -e "s|OWNER\.github\.io/ai-computing-encyclopedia|${OWNER}.github.io/${REPO}|g" \
    -e "s|@Iamhifza|@${OWNER}|g" \
    "$file"
  rm -f "${file}.bak"
done

echo "→ Verifying the corpus still builds"
if command -v enc >/dev/null 2>&1; then
  enc validate
else
  PYTHONPATH=tools python3 -m encyclopedia validate
fi

if [[ ! -d .git ]]; then
  echo "→ Initialising git"
  git init -b main
fi

git add -A
if git diff --cached --quiet; then
  echo "→ Nothing to commit"
else
  git commit -m "Initial commit: AI & Computing Encyclopedia

Structured concept corpus with validation, site generation and a JSON API.
Entries are the source of truth; every view is generated from them."
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin "https://github.com/${OWNER}/${REPO}.git"
  echo "→ Added remote origin"
fi

cat <<NEXT

Done. Next steps:

  1. Create an empty repository at https://github.com/new named "${REPO}"
     (no README, no .gitignore, no licence -- this repo has them).
  2. git push -u origin main
  3. Repository → Settings → Pages → Source: "GitHub Actions"

The site will publish to https://${OWNER}.github.io/${REPO}/ on that push.
NEXT
