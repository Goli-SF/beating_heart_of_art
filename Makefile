.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	# @pip uninstall -y <PackageNAME> || :
	# @pip install -e .


run_api:
	uvicorn taxifare.api.fast:app --reload
