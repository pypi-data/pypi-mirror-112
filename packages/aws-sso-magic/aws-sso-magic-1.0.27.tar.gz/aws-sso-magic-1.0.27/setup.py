# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_sso_magic']

package_data = \
{'': ['*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'aws-error-utils>=1.0.4,<2.0.0',
 'aws-sso-lib>=1.7.0,<2.0.0',
 'boto3>=1.17.20,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['aws-sso-magic = aws_sso_magic.cli:cli']}

setup_kwargs = {
    'name': 'aws-sso-magic',
    'version': '1.0.27',
    'description': 'Magic credentials on the AWS CLI home using AWS SSO login',
    'long_description': '#\n# aws-sso-magic tool cli \nThis tool update the aws credentials file for the default profile from the aws sso login.\n\nThis solution mixed the following repositories:\n\n1. [aws-sso-util](https://github.com/benkehoe/aws-sso-util) AWS SSO has some rough edges, and aws-sso-util is here to smooth them out, hopefully temporarily until AWS makes it better.\n2. [aws-sso-credentials](https://github.com/NeilJed/aws-sso-credentials) A simple Python tool to simplify getting short-term credential tokens for CLI/Boto3 operations when using AWS SSO.\n\n### Content of the repository\n\n- [src](src) - The main folder with the aws_sso_magic folder with the .py files & the requirements.txt.\n    - [aws_sso_magic](src/aws_sso_magic)\n- [docker-build.sh](cli/docker-build.sh) - A docker build tool (Linux/MacOS) to build the docker image locally.\n    ```bash\n    sudo ./docker-build.sh\n    ```     \n- [pyproject.toml](pyproject.toml) - The metadata file with the dependencies and application information.    \n- [Dockerfile](Dockerfile) - The docker file with the instructions to build the aws-sso-magic cli.\n- [eks-login](utils/eks-login) - A script tool to add on the /usr/local/bin (Only for linux/macOS or Windows WSL).\n    ```bash\n    eks-login develop-readonly\n    ```     \n#\n## Installation \n### Using pyp installer\n#### - Prerequisites\n1. [Python 3.9](https://www.python.org/downloads/) installed.\n2. [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed, please click on the link depending of your OS.\n\n#### - Installation\n\n1. Follow the pyp [aw-sso-magic](https://pypi.org/project/aws-sso-magic/) project instructions to install it.\n\n    Note: If you want upgrade it, please run this `pip install aws-sso-magic --upgrade`\n\n### Using Docker\n\n1. Please follow the instructions from the docker hub repository of [aws_sso_magic](https://hub.docker.com/r/javiortizmol/aws_sso_magic)\n\n#\n## Configuration Instructions\nThese steps will create the config files on the paths $HOME/.aws and $HOME/.aws-sso-magic.\n\n1. Execute the following command to configure the sso tool: `aws-sso-magic configure`\n2. Type the following information:\n    - SSO start URL\n    - SSO Region\n    - Select the default profile of SSO\n    - CLI default client Region\n    - CLI default output format\n    - CLI profile name. Eg: default\n    - Enter only the name of the proxy role to use by default. Eg: MyAdminRole or just press Enter (This option will mandatory for the --eks flag)\n3. Optional: In case that you want to set an account alias, you can modify the file on $HOME/.aws-sso-magic/config adding the [AliasAccounts] section with key (account name) and value (alias account) Eg:\n    ```\n    [AliasAccounts]\n    test1 = dev\n    test2 = qa\n    test3 = staging\n    test4 = prod\n    ```\n    making the above configuration, it will now show the aliases in the profile selection menu when aws-sso-magic login command is executed.\n    ```\n    [?] Please select an AWS config profile:    \n      aws-sso\n      default\n      dev-admin\n    > qa-admin \n      staging-admin   \n      prod-admin\n    ```\n\n#\n## How to use it\n\n1. Execute the following command to select and log into the aws accounts: `aws-sso-magic login`\n3. Execute the following command to log: `aws-sso-magic login` and select the profile to use or `aws-sso-login login --profile myprofile` if you already know the profile name.\n\n## How to use it for eks support\n### - Prerequisites\n1. [kubectl](https://kubernetes.io/docs/tasks/tools/) installed.\n2. `aws-sso-magic login` or `aws-sso-login login --profile myprofile` executed previouly.\n\n### - Instructions\n1. Go to the file $HOME/.aws-sso-magic/config and replace the string "replacethis" on the section default-proxy-role-name if you want to use that role name for all profiles.\n    ```\n    [default-proxy-role-name]\n    proxy_role_name = replacethis    \n    ```\n\n    or just add the profile section in the file. Eg:\n\n    ```\n    [myprofile]\n    proxy_role_name = myrolename\n    ```\n2. Execute the following command to select and log the eks cluster: `aws-sso-magic login --eks` or if you have configured an aws account as trusted entity having granted to assume roles on the rest of the accounts from there, please execute `aws-sso-magic login` selecting profile (account and role configured as trusted identity) and then execute `aws-sso-magic login --eks --eks-profile env-eks-profile`. Eg:\n    ```\n    aws-sso-magic login --profile main-admin\n    aws-sso-magic login --eks --eks-profile qa-admin\n    ```\n3. Please select the EKS cluster or send the cluster name using the flag --cluster. Eg: `aws-sso-magic login --eks --cluster myekscluster`\n4. Copy and paste the commands according to your OS.\n    \n    NOTE: If you will select another profile, please first unset the AWS_PROFILE environment variable or close this terminal and open a new one\n#\n## Links\n### - pypi.org\n- [aw-sso-magic](https://pypi.org/project/aws-sso-magic/) \n### - [Docker Hub](https://hub.docker.com/u/javiortizmol)\n- [aws_sso_magic](https://hub.docker.com/r/javiortizmol/aws_sso_magic)\n',
    'author': 'Javier Ortiz',
    'author_email': 'jahor2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/javiortizmol/aws-sso-magic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
