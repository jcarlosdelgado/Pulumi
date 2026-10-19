#!/bin/bash
export PATH="$PATH:/c/Program Files (x86)/Pulumi"
if [ -f .env ]; then set -a; source .env; set +a; fi
pulumi up "$@"
