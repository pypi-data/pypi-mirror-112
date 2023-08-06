export GIT_PYTHON_REFRESH=quiet
dvc init --no-scm
dvc remote add --default ds-ml-artifacts gs://dozi-stg-ds-apps-1-ds-apps-ds-ml-artifacts/{name-your-artifacts}
dvc remote modify ds-ml-artifacts projectname dozi-stg-ds-apps-1
dvc config core.analytics false

dvc status
dvc fetch
dvc pull
#python script_load_model.py
