#!/bin/bash

docker run --env-file `pwd`/dev_env.vars -it --rm -v `pwd`/src:/application rotation-helper-app:dev bash