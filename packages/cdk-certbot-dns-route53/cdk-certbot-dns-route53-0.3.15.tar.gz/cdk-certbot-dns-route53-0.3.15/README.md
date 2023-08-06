[![NPM version](https://badge.fury.io/js/cdk-certbot-dns-route53.svg)](https://badge.fury.io/js/cdk-certbot-dns-route53)
[![PyPI version](https://badge.fury.io/py/cdk-certbot-dns-route53.svg)](https://badge.fury.io/py/cdk-certbot-dns-route53)
[![Release](https://github.com/neilkuan/cdk-certbot-dns-route53/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/neilkuan/cdk-certbot-dns-route53/actions/workflows/release.yml)

# cdk-certbot-dns-route53

**cdk-certbot-dns-route53** is a CDK construct library that allows you to create [Certbot](https://github.com/certbot/certbot) Lambda Function on AWS with CDK, and setting schedule cron job to renew certificate to store on S3 Bucket.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_route53 as r53
import aws_cdk.aws_s3 as s3
import aws_cdk.core as cdk
from cdk_certbot_dns_route53 import CertbotDnsRoute53Job

dev_env = {
    "account": process.env.CDK_DEFAULT_ACCOUNT,
    "region": process.env.CDK_DEFAULT_REGION
}

app = cdk.App()

stack = cdk.Stack(app, "lambda-certbot-dev", env=dev_env)

CertbotDnsRoute53Job(stack, "Demo",
    certbot_options={
        "domain_name": "*.example.com",
        "email": "user@example.com"
    },
    zone=r53.HostedZone.from_hosted_zone_attributes(stack, "myZone",
        zone_name="example.com",
        hosted_zone_id="mockId"
    ),
    destination_bucket=s3.Bucket.from_bucket_name(stack, "myBucket", "mybucket")
)
```

### Example: Invoke Lambda Function log.

![](./images/lambda-logs.png)

### Example: Renew certificate to store on S3 Bucket

![](./images/s3-bucket.png)
