dvc add --recursive pipeline/artifacts
git add pipeline/artifacts
git commit -m "Add data and artifacts to DVC"
dvc push
