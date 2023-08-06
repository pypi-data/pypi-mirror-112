# AWS Service Catalog Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[AWS Service Catalog](https://docs.aws.amazon.com/servicecatalog/latest/dg/what-is-service-catalog.html)
enables organizations to create and manage catalogs of products for their end users that are approved for use on AWS.

## Table Of Contents

* [Portfolio](#portfolio)

  * [Granting access to a portfolio](#granting-access-to-a-portfolio)
  * [Sharing a portfolio with another AWS account](#sharing-a-portfolio-with-another-aws-account)
* [Product](#product)

The `@aws-cdk/aws-servicecatalog` package contains resources that enable users to automate governance and management of their AWS resources at scale.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_servicecatalog as servicecatalog
```

## Portfolio

AWS Service Catalog portfolios allow admins to manage products that their end users have access to.
Using the CDK, a new portfolio can be created with the `Portfolio` construct:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
servicecatalog.Portfolio(self, "MyFirstPortfolio",
    display_name="MyFirstPortfolio",
    provider_name="MyTeam"
)
```

You can also specify properties such as `description` and `acceptLanguage`
to help better catalog and manage your portfolios.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
servicecatalog.Portfolio(self, "MyFirstPortfolio",
    display_name="MyFirstPortfolio",
    provider_name="MyTeam",
    description="Portfolio for a project",
    accept_language=servicecatalog.AcceptLanguage.EN
)
```

Read more at [Creating and Managing Portfolios](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/catalogs_portfolios.html).

A portfolio that has been created outside the stack can be imported into your CDK app.
Portfolios can be imported by their ARN via the `Portfolio.fromPortfolioArn()` API:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
portfolio = servicecatalog.Portfolio.from_portfolio_arn(self, "MyImportedPortfolio", "arn:aws:catalog:region:account-id:portfolio/port-abcdefghi")
```

### Granting access to a portfolio

You can manage end user access to a portfolio by granting permissions to `IAM` entities like a user, group, or role.
Once resources are deployed end users will be able to access them via the console or service catalog CLI.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam


user = iam.User(self, "MyUser")
portfolio.give_access_to_user(user)

role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountRootPrincipal()
)
portfolio.give_access_to_role(role)

group = iam.Group(self, "MyGroup")
portfolio.give_access_to_group(group)
```

### Sharing a portfolio with another AWS account

A portfolio can be programatically shared with other accounts so that specified users can also access it:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
portfolio.share_with_account("012345678901")
```

## Product

Products are the resources you are allowing end users to provision and utilize.
The CDK currently only supports adding products of type Cloudformation product.
Using the CDK, a new Product can be created with the `CloudFormationProduct` construct.
`CloudFormationTemplate.fromUrl` can be utilized to create a Product using a Cloudformation template directly from an URL:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[{
        "product_version_name": "v1",
        "cloud_formation_template": servicecatalog.CloudFormationTemplate.from_url("https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/ServiceCatalog/Product.yaml")
    }
    ]
)
```

A `CloudFormationProduct` can also be created using a Cloudformation template from an Asset.
Assets are files that are uploaded to an S3 Bucket before deployment.
`CloudFormationTemplate.fromAsset` can be utilized to create a Product by passing the path to a local template file on your disk:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
product = servicecatalog.CloudFormationProduct(self, "MyFirstProduct",
    product_name="My Product",
    owner="Product Owner",
    product_versions=[{
        "product_version_name": "v1",
        "cloud_formation_template": servicecatalog.CloudFormationTemplate.from_url("https://raw.githubusercontent.com/awslabs/aws-cloudformation-templates/master/aws/services/ServiceCatalog/Product.yaml")
    }, {
        "product_version_name": "v2",
        "cloud_formation_template": servicecatalog.CloudFormationTemplate.from_asset(path.join(__dirname, "development-environment.template.json"))
    }
    ]
)
```
