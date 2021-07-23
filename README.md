# Nautobot Chatops Extension Arista

An extension for [Nautobot](https://github.com/nautobot/nautobot) [Chatops Plugin](https://github.com/nautobot/nautobot-plugin-chatops/)

### Build Status

| Branch      | Status |
|-------------|------------|
| **main** | [![Build Status](https://travis-ci.com/networktocode-llc/nautobot-chatops-extension-cloudvision.svg?token=BknroZ7vxquiYcUvP8RC&branch=main)](https://travis-ci.com/networktocode-llc/nautobot-chatops-extension-cloudvision) |
| **develop** | [![Build Status](https://travis-ci.com/networktocode-llc/nautobot-chatops-extension-cloudvision.svg?token=BknroZ7vxquiYcUvP8RC&branch=develop)](https://travis-ci.com/networktocode-llc/nautobot-chatops-extension-cloudvision) |

The extension is available as a Python package in PyPI and can be installed with pip

```shell
pip install git+https://github.com/networktocode-llc/nautobot-chatops-extension-cloudvision.git
```

This ChatOps Extension to Nautobot ChatOps Plugin requires environment variables to be set up depending on if you are using a CVAAS (Cloudvision as a Service) or Cloudvision on-premise.

For CVAAS the following environment variables must be set.

- `CVAAS_TOKEN`: Token generated from CVAAS service account. Documentation for that process can be found [here](https://www.arista.com/assets/data/pdf/qsg/qsg-books/QS_CloudVision_as_a_Service.pdf) in section 1.7

For on premise instance of Cloudvision, these environment variables must be set.

- `CVP_USERNAME`: The username that will be used to authenticate to Cloudvision.
- `CVP_PASSWORD`: The password for the configured username.
- `CVP_HOST`: The IP or hostname of the on premise Cloudvision appliance.
- `CVP_INSECURE`: If this is set to `True`, the appliance cert will be downloaded and automatically trusted. Otherwise, the appliance is expected to have a valid certificate.
- `ON_PREM`: By default this is set to False, this must be changed to `True` if using an on-prem instance of Cloudvision.

Once you have updated your environment file, restart both nautobot and nautobot-worker

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart nautobot nautobot-worker
```

## Usage

### Nautobot Config

You must first update the Nautobot configuration file with a new entry in the `PLUGINS_CONFIG` dictionary.

```python
PLUGINS_CONFIG = {
    'nautobot_chatops': {
        'enable_slack': True,
        'slack_api_token': os.getenv("SLACK_API_TOKEN"),
        'slack_signing_secret': os.getenv("SLACK_SIGNING_SECRET")
    },
    'nautobot_plugin_chatops_cloudvision' : {
        'cvaas_token': os.getenv("CVAAS_TOKEN"),
        'cvp_username': os.getenv("CVP_USERNAME"),
        'cvp_password': os.getenv("CVP_PASSWORD"),
        'cvp_host': os.getenv("CVP_HOST"),
        "cvp_insecure": os.getenv("CVP_INSECURE"),
        'on_prem': os.getenv("ON_PREM")
    }
}
```

After that, you must update environment variables depending on if you are using a CVAAS (Cloudvision as a Service) or Cloudvision on-premise. To update environment variables in Nautobot check out our blog post [here](http://blog.networktocode.com/post/creating-custom-chat-commands-using-nautobot-chatops/)

For CVAAS the following environment variables must be set.

- `CVAAS_TOKEN`: Token generated from CVAAS service account. Documentation for that process can be found [here](https://www.arista.com/assets/data/pdf/qsg/qsg-books/QS_CloudVision_as_a_Service.pdf) in section 1.7

For on premise instance of Cloudvision, these environment variables must be set.

- `CVP_USERNAME`: The username that will be used to authenticate to Cloudvision.
- `CVP_PASSWORD`: The password for the configured username.
- `CVP_HOST`: The IP or hostname of the on premise Cloudvision appliance.
- `CVP_INSECURE`: If this is set to `True`, the appliance cert will be downloaded and automatically trusted. Otherwise, the appliance is expected to have a valid certificate.
- `ON_PREM`: By default this is set to False, this must be changed to `True` if using an on-prem instance of Cloudvision.

Once you have updated your environment file, restart both nautobot and nautobot-worker

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart nautobot nautobot-worker
```

### Command setup

Add a slash command to Slack called `/cloudvision`.
See the [nautobot-chatops installation guide](https://github.com/nautobot/nautobot-plugin-chatops/blob/develop/docs/chat_setup.md) for instructions on adding a slash command to your Slack channel.

The following commands are available:

- `get-devices-in-container [container-name]`: Retrieves all the devices assigned to the specificied container.
- `get-configlet [configlet-name]`: Get the configuration of the specified configlet.
- `get-device-configuration [device-name]`: Get the configuration of the specified device.
- `get-task-logs [task-id]`: Get the logs of the specified task.
- `get-applied-configlets [filter-type] [filter-value]`: Get applied configlets to either a specified container or device.
- `get-active-events [filter-type] [filter-value] [start-time] [end-time]`: Get active events in a given time frame. Filter-type can be filtered by device, type or severity. Filter-value is dynamically created based on the filter-type. Start-time accepts ISO time format as well as relative time inputs. Examples of that are  `-2w`, `-2d`, `-2h` which will go back two weeks, two days and two hours, respectively.
- `get-applied-image-bundles [filter-type] [image-bundle-name]`: Gets the devices and containers an image bundle is applied to. Can also specify the `all` parameter to get a list of all the image bundles on Cloudvision.
- `get-device-cve [device-name]`: Gets all the CVEs of the specified device. Can also specifiy the `all` parameter to get a count of CVE account for each device.

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

### Development Environment

The development environment can be used in 2 ways. First, with a local poetry environment if you wish to develop outside of Docker. Second, inside of a docker container.

#### Invoke tasks

The [PyInvoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment.  There are a few configuration parameters which can be passed to PyInvoke to override the default configuration:

* `nautobot_ver`: the version of Nautobot to use as a base for any built docker containers (default: 1.0.1)
* `project_name`: the default docker compose project name (default: nautobot_plugin_chatops_cloudvision)
* `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.6)
* `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers)
* `compose_dir`: the full path to a directory containing the project compose files
* `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information)

Using PyInvoke these configuration options can be overridden using [several methods](http://docs.pyinvoke.org/en/stable/concepts/configuration.html).  Perhaps the simplest is simply setting an environment variable `INVOKE_NAUTOBOT-CHATOPS-EXTENSION-ARISTA_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override.  The only exception is `compose_files`, because it is a list it must be overridden in a yaml file.  There is an example `invoke.yml` in this directory which can be used as a starting point.

#### Local Poetry Development Environment

1. Copy `development/creds.example.env` to `development/creds.env` (This file will be ignored by git and docker)
2. Uncomment the `POSTGRES_HOST`, `REDIS_HOST`, and `NAUTOBOT_ROOT` variables in `development/creds.env`
3. Create an invoke.yml with the following contents at the root of the repo:

```shell
---
nautobot_plugin_chatops_cloudvision:
  local: true
  compose_files:
    - "docker-compose.requirements.yml"
```

3. Run the following commands:

```shell
poetry shell
poetry install --extras nautobot
export $(cat development/dev.env | xargs)
export $(cat development/creds.env | xargs)
invoke start && sleep 5
nautobot-server migrate
```

> If you want to develop on the latest develop branch of Nautobot, run the following command: ``poetry add git+https://github.com/nautobot/nautobot@develop``. After the ``@`` symbol must match either a branch or a tag.

4. You can now run nautobot-server commands as you would from the [Nautobot documentation](https://nautobot.readthedocs.io/en/latest/) for example to start the development server:

```shell
nautobot-server runserver 0.0.0.0:8080 --insecure
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

#### Docker Development Environment

This project is managed by [Python Poetry](https://python-poetry.org/) and has a few requirements to setup your development environment:

1. Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2. Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.

Once you have Poetry and Docker installed you can run the following commands to install all other development dependencies in an isolated python virtual environment:

```shell
poetry shell
poetry install
invoke start
```

Nautobot server can now be accessed at [http://localhost:8080](http://localhost:8080).

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`.

Each command can be executed with `invoke <command>`. Environment variables `INVOKE_NAUTOBOT_CHATOPS_PLUGIN_CLOUDVISION_PYTHON_VER` and `INVOKE_NAUTOBOT_CHATOPS_PLUGIN_CLOUDVISION_NAUTOBOT_VER` may be specified to override the default versions. Each command also has its own help `invoke <command> --help`

#### Docker dev environment

```no-highlight
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart Nautobot and its dependencies.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

#### Utility

```no-highlight
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
```

#### Testing

```no-highlight
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           This will run flake8 for the specified name and Python version.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

## Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)
