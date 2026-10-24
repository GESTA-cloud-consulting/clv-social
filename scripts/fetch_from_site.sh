#!/usr/bin/env bash
# Download photos from chiantiluxuryvillas.com into incoming/<job>/ via the
# "Fetch site media" GitHub Action (Claude sessions cannot reach the site directly).
#
# Usage: scripts/fetch_from_site.sh <job> <list.txt>
#   <job>       folder name, e.g. social-clv-1118
#   <list.txt>  one line per photo: "<https://chiantiluxuryvillas.com/wp-content/uploads/...> <NN-name.webp>"
# Prints the folder and the status ("ok" or "failed"); exits 1 on timeout.
set -euo pipefail
job="$1"; list="$2"
cd "$(git rev-parse --show-toplevel)"
git pull -q --rebase origin main
rm -rf "incoming/$job"
mkdir -p fetch
cp "$list" "fetch/$job.txt"
git add "fetch/$job.txt"
git -c user.name="GESTA Cloud Consulting" -c user.email="info@gesta.cc" commit -qm "Fetch $job"
git push -q origin main
head=$(git rev-parse HEAD)
for i in $(seq 1 60); do            # up to ~5 minutes
  sleep 5
  remote=$(git ls-remote origin main | cut -f1)
  if [ "$remote" != "$head" ]; then
    git pull -q --rebase origin main
    if [ -f "incoming/$job/_status.txt" ]; then
      echo "incoming/$job $(cat "incoming/$job/_status.txt")"
      exit 0
    fi
    head="$remote"
  fi
done
echo "timeout: check https://github.com/GESTA-cloud-consulting/clv-social/actions" >&2
exit 1
