#!/bin/bash

python <<EOF
print("<-----build.sh - build/launch sevrer in one step------>")
print("\n\tFlushing out old fixture\n")
EOF

python manage.py flush

python <<EOF
print("\n\tChecking for model updates\n")
EOF

python manage.py makemigrations

python <<EOF
print("\n\tApplying model migrations\n")
EOF

python manage.py migrate

python <<EOF
print("\n\tLoading fixture\n")
EOF

python manage.py loaddata CMPT350/fixtures/dump.json

python <<EOF
print("<-----build.sh - end script------>")
EOF

