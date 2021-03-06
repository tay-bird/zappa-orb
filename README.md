# Zappa Orb ![CircleCI Status](https://circleci.com/gh/tay-bird/zappa-orb.svg "CircleCI Status")

Easily update and manage your [Zappa](https://github.com/Miserlou/Zappa "Zappa") deployments in your [CircleCI](https://circleci.com/ "CircleCI") jobs and workflows.

Learn more about [Orbs](https://github.com/CircleCI-Public/config-preview-sdk/blob/master/docs/using-orbs.md "orb").

## Tutorial

Follow the [Zappa tutorial](https://github.com/Miserlou/Zappa#installation-and-configuration "Zappa tutorial") to set up a new Zappa project. Then, configure a CircleCI job in `.circleci/config.yml`:

```yaml
version: 2.1

orbs:
  zappa: borb/zappa@dev:master

jobs:
  - zappa/zappa-deploy:
      stage: "dev"
      python_version: "3.6"
      filters:
        branches:
          only: master
```

Push your changes to master and check your build output. Your tutorial app should be available at a URL like:

```
https://<random_id>.execute-api.<aws_region>.amazonaws.com/dev
```

For a complete example, see [tay-bird/zappa-circle-demo](https://github.com/tay-bird/zappa-circle-demo "tay-bird/zappa-circle-demo").

## Documentation

For more information about how to use this Orb, please see the [borb/zappa](https://circleci.com/orbs/registry/orb/borb/zappa "borb/zappa") docs.
