
######################################################################################################################################################

jq -n . >/dev/null 2>&1 || die "Need to install jq"

unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

creds=$(aws sts assume-role --role-arn arn:aws:iam::517634383609:role/edl-east-dataops --role-session-name proxy-emr-session ) || die "Couldn't do Assume-Role"
AWS_ACCESS_KEY_ID=$(echo "${creds}" | jq -r .Credentials.AccessKeyId)
AWS_SECRET_ACCESS_KEY=$(echo "${creds}" | jq -r .Credentials.SecretAccessKey)
AWS_SESSION_TOKEN=$(echo "${creds}" | jq -r .Credentials.SessionToken)
expiration=$(echo "${creds}" | jq -r .Credentials.Expiration)

export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" AWS_SESSION_TOKEN="$AWS_SESSION_TOKEN";

######mdm-files###########

aws s3api head-object --bucket us-gov-cms-mdm-dataproduct-prod --key metadata/mdm_pmi_spp_2021-07-30T1654.xlsx || mdm_not_exist=true
if [ $mdm_not_exist ]; then
  echo "mdm file does not exist"
else
  aws s3 cp s3://us-gov-cms-mdm-dataproduct-prod/metadata/mdm_pmi_spp_2021-07-30T1654.xlsx /home/ec2-user/amundsendatabuilder/example/source_files/mdm_pmi_spp_2021-07-30T1654.xlsx
fi


#####bic-files###########

aws s3api head-object --bucket 517634383609-east-edl-amundsen --key amundsen/data-dictionaries/bic_2021-07-29T1306.xlsx || bic_not_exist=true
if [ $bic_not_exist ]; then
  echo "bic file does not exist"
else
  aws s3 cp s3://517634383609-east-edl-amundsen/amundsen/data-dictionaries/bic_2021-07-29T1306.xlsx /home/ec2-user/amundsendatabuilder/example/source_files/bic_2021-07-29T1306.xlsx
fi

