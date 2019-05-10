Installation

Ensure you have Python 3 and the package manager pip installed.

Run the following command to access the Kaggle API using the command line:

pip install kaggle (You may need to do pip install --user kaggle on Mac/Linux. This is recommended if problems come up during the installation process.) Installations done through the root user (i.e. sudo pip install kaggle) will not work correctly unless you understand what you're doing. Even then, they still might not work. User installs are strongly recommended in the case of permissions errors.

You can now use the kaggle command as shown in the examples below.

If you run into a kaggle: command not found error, ensure that your python binaries are on your path. You can see where kaggle is installed by doing pip uninstall kaggle and seeing where the binary is. For a local user install on Linux, the default location is ~/.local/bin. On Windows, the default location is $PYTHON_HOME/Scripts.

IMPORTANT: We do not offer Python 2 support. Please ensure that you are using Python 3 before reporting any issues.

API credentials

To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. Then go to the 'Account' tab of your user profile (https://www.kaggle.com/<username>/account) and select 'Create API Token'. This will trigger the download of kaggle.json, a file containing your API credentials. Place this file in the location ~/.kaggle/kaggle.json (on Windows in the location C:\Users\<Windows-username>\.kaggle\kaggle.json - you can check the exact location, sans drive, with echo %HOMEPATH%). You can define a shell environment variable KAGGLE_CONFIG_DIR to change this location to $KAGGLE_CONFIG_DIR/kaggle.json (on Windows it will be %KAGGLE_CONFIG_DIR%\kaggle.json).

For your security, ensure that other users of your computer do not have read access to your credentials. On Unix-based systems you can do this with the following command:

chmod 600 ~/.kaggle/kaggle.json

You can also choose to export your Kaggle username and token to the environment:

export KAGGLE_USERNAME=datadinosaur
export KAGGLE_KEY=xxxxxxxxxxxxxx
In addition, you can export any other configuration value that normally would be in the $HOME/.kaggle/kaggle.json in the format 'KAGGLE_' (note uppercase).
For example, if the file had the variable "proxy" you would export KAGGLE_PROXY and it would be discovered by the client.

