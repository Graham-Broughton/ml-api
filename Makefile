include .env
export

SHELL = bash 
.SHELLFLAGS = -ec -o pipefail

MODEL_DIR=$(PWD)/models
MODEL_MARKER=$(MODEL_DIR)/.downloaded
WANDB_REGISTERED_MODEL = "${MODEL}-${RESOLUTION}""



.PHONY: get_deploy_model local_deploy

#################################################
### Deploy
#################################################

# The target that depends on MODEL_MARKER
get_deploy_model: $(MODEL_MARKER)
	@echo "Model is already downloaded."

# Deploy the model to a local server using ngrok
local_deploy: get_deploy_model
	@echo "Deploying model..."
	@cd mush_app && pipenv run python app.py & 
	@ngrok http 5000
	@echo "Finished deploying model..."

# Download the latest registered model from wandb if it doesn't exist
$(MODEL_MARKER):
	@echo "Downloading model..."
	@mkdir -p $(MODEL_DIR)
	@pipenv run wandb artifact get model-registry/$(WANDB_REGISTERED_MODEL):latest --root $(MODEL_DIR)
	@touch $(MODEL_MARKER)
