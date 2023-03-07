.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
# reinstall_package:
# 	# @pip uninstall -y projects || :
# 	# @pip install -e .

run_api:
	uvicorn projects.api.fastapi:app --reload
