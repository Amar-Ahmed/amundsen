#!/bin/bash

account_number=$(aws sts get-caller-identity \
            --query "Account" \
            --output text)

# DEV.
if [ "$account_number" = "310946103770" ]; then
        hosted_zone_id="Z0492289QZDLQJX5S1KD"

# TEST.
elif [ "$account_number" = "782747344429" ]; then
        hosted_zone_id="Z04203743J7NP8X4WTQOU"

# IMPL.
elif [ "$account_number" = "724285879981" ]; then
        hosted_zone_id="Z02320412WND0A2KKZFNC"

# PROD.
elif [ "$account_number" = "517634383609" ]; then
        hosted_zone_id="Z0942889XBGJEZ03JRDO"

else echo "Invalid Account Number!"
fi

# get elasticsearch IP.
es_ip=$(aws route53 list-resource-record-sets \
            --hosted-zone-id $hosted_zone_id \
            --query "ResourceRecordSets[?starts_with(Name,'elasticsearch')].ResourceRecords[].Value" \
            --output text)

# echo $es_ip

# get neo4j IP.
nj_ip=$(aws route53 list-resource-record-sets \
            --hosted-zone-id $hosted_zone_id \
            --query "ResourceRecordSets[?starts_with(Name,'neo4j')].ResourceRecords[].Value" \
            --output text)

# echo $nj_ip

# remove old ips.
sed -i '/PROXY/d' .bash_profile

# update new ips.
sed -i -e '$a\
export CREDENTIALS_ELASTICSEARCH_PROXY_HOST='"$es_ip"'\
export CREDENTIALS_NEO4J_PROXY_HOST='"$nj_ip"'' .bash_profile