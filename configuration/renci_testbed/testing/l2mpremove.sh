#!/bin/bash
policy_number=$1
curl \
-b cookie-mcevik.txt \
-H "Content-Type: application/json" \
-X DELETE http://atlanticwave-sdx-controller.renci.ben:5000/api/v1/policies/number/${policy_number}
