.PHONY: info init create_project get_alm_settings list_all

info:
	@echo "Usage: make [init|run]"

init:
	@echo "Initializing..."
	@pip install -r requirements.txt
	@echo $(SONARQUBE_CONFIG) | base64 -d > config.yaml

create_project: init
	@echo "Running..."
	@python main.py --is_create_project=$(IS_CREATE_PROJECT) \
		--gitlab_project_key=$(GITLAB_PROJECT_KEY) \
		--is_create_binding=$(IS_CREATE_BINDING)

get_alm_settings: init
	@python main.py

list_all: init
	@python main.py --is_list_all=$(IS_LIST_ALL)
