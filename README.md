
# Setting up a Linux development machine for Sweatscore API development

## Install Linux system utilities and libraries

### 1. Command line utilities.

```
sudo apt install wget curl git
```

### 2. Build utilities.

```
sudo apt install llvm make build-essential
```

### 3. Dependencies and libraries for building Python interpreters.

Edit the file `/etc/apt/sources.list` and add the following line to the end:

```
deb-src http://archive.ubuntu.com/ubuntu/ <UBUNTU_CODENAME> main
```

Replace `UBUNTU_CODENAME` with the Ubuntu release name, then run `sudo apt-get update`
to read the list of build dependencies.

Run `sudo apt-get build-dep python3.<latest version>` to install the system dependencies
and libraries needed to build Python interpreters.

### 3. Extra dependencies.

Some extra dependencies and libraries are needed. Install with:

```
sudo apt install libpq-dev libssl-dev libxml2-dev libxmlsec1-dev \
zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl
```

## Install asdf

### 1. Run the following command in your home directory.

**NOTE:** Check the asdf website at https://asdf-vm.com
for the latest branch and version information.

```
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch <latest version>
```

### 2. Add the following lines to the end of ~/.bashrc.

```
source $HOME/.asdf/asdf.sh
source $HOME/.asdf/completions/asdf.bash
```

### 3. Install the Python plug-in for asdf.

More information about the plug-in can be found at https://github.com/asdf-community/asdf-python

```
asdf plugin add python
```

### 4. Install a global Python interpreter

**NOTE:** The Python interpreter in use by the project may or may not be the latest version of Python.

To see a list of all the different Python interpreters available to asdf:

```
asdf list all <name> [<version>]

```

To see a list of the interpreters already installed locally:

```
asdf list <name> [version]
```

To *globally* install the latest Python interpreter, or, a specific version:

```
asdf install python latest
```

For example:

```
asdf install python 3.12.2
```

## Create an SSH key and add it to your SSH agent

### 1. Make sure the .ssh directory exists with the proper permissions.

```
mkdir -p ~/.ssh && chmod 700 ~/.ssh
```

### 2. From a command shell, cd into the SSH directory and generate the key using
the following command, substituting your GitHub email address.

```
ssh-keygen -t ed25519 -C "<your_email>@digiadsapp.com"
```

Save the key into the default .ssh directory using the following naming convention.
Remember to type the full path:

```
/home/<your_linux_username>/.ssh/<your_email>@github
```

Enter a passphrase when prompted. You will be prompted to re-enter the passphrase.

### 3. Start the SSH agent and add the key.

```
eval "$(ssh-agent -s)"
```

### 4. Add the key to the SSH agent.

```
ssh-add ~/.ssh/<your_email>@github
```

### 5. Add the SSH key to your GitHub profile.

Add the key to the settings section of your GitHub account under and test the connection.

```
ssh -T git@github.com
```

Verify that the fingerprint in the message matches GitHub's public key fingerprint.

## Instructions to set-up www.digiadsapp.com.

### Clone the project from GitHub

The directory structure must reside within your dedicated all projects directory. The Digi-Ads specific
directory should be named DigiAds or DigiAdsApp. Individual repositories will be cloned within that
directory, with the exception of programs and websites, which will reside within respective nested
directories.

The parent directory for www.digiadsapp.com should be:

```
~/<your_projects_directory>/DigiAds/websites
```

## Install a Python interpreter into the project directory

1. From a command shell, cd into the project directory.

2. Use asdf to switch to the appropriate Python interpreter used by the shell.

```
asdf shell python <version>
```

3. Create a Python virtual environment, named 'python', in the project directory.

```
python -m venv python
```

4. Use asdf to deactivate the global Python interpreter.

```
asdf shell python --unset
```

5. Activate the Python virtual interpreter.

```
. python/bin/activate
```

6. Update PIP and install the 'wheel' package.

```
pip install --upgrade pip
pip install wheel
```

7. Install project requirements.

```
pip install -r requirements.lock
```

The project should be ready to run.

## PIP package requirements

fastapi
psycopg2-binary
sqlalchemy
alembic
uvicorn
requests
cryptography
pydantic-extra-types
phonenumbers
email-validator

## Running tests

To run all tests in the test files:

  unittest.main()

To create a test suite:

  def my_test_class_test_suite():

    test_suite = unittest.TestSuite()

    test_suite.addTest(MyClassTests('test_my_test_case'))
    test_suite.addTest(MyClassTests('test_another_test_case'))

    return test_suite

To run the test suite:

  test_runner = unittest.TextTestRunner()

  test_runner.run(my_test_class_test_suite())
