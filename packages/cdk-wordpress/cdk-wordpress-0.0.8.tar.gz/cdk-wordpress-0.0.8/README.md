# cdk-wordpress

[![NPM version](https://badge.fury.io/js/cdk-wordpress.svg)](https://www.npmjs.com/package/cdk-wordpress)
[![PyPI version](https://badge.fury.io/py/cdk-wordpress.svg)](https://pypi.org/project/cdk-wordpress)
![Release](https://github.com/clarencetw/cdk-wordpress/workflows/Release/badge.svg)

![npm](https://img.shields.io/npm/dt/cdk-wordpress?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-wordpress?label=pypi&color=blue)

A CDK construct library to deploy WordPress

## How do use

Install your package manager:

```sh
yarn add cdk-wordpress
```

### TypeScript Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_wordpress import WordPress

wordpress = WordPress(stack, "WordPressEcs")

# Get WordPress endpoint
CfnOutput(stack, "Endpoint", value=wordpress.endpoint)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```
