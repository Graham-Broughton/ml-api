#!/usr/bin/env bash

echo $WANDB_API_KEY

echo $(wandb login $WANDB_API_KEY)

echo $(wandb artifact get model-registry/$1:latest --root ./models)