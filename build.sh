#!/bin/bash

set -e

workpath="json_data"
reponame="vscape-clues"
username="altbdoor"
branchname="json_data"

echo "Cleaning up"
rm -rf "./$workpath"
mkdir "./$workpath"
cd "./$workpath"

echo "Calling script"
python ../scrape.py

echo "Setting up git"
git init
git config user.name "$username"
git config user.email "lancersupraskyline@gmail.com"

timestamp=$(date '+%Y-%m-%dT%H:%M:%S%z')
git add .
git commit -m "[appveyor] updated data on $timestamp"

echo "Pushing"
git push --force "https://$username:${GH_TOKEN}@github.com/$username/$reponame.git" master:$branchname

echo "Done"
