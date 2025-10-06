#/bin/bash
aws bedrock create-inference-profile \
  --inference-profile-name "test profiles" \
  --model-source copyFrom="arn:aws:bedrock:ap-northeast-1:<account id>:inference-profile/apac.anthropic.claude-3-sonnet-20240229-v1:0" \
  --no-cli-pager
