# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['passrack']
install_requires = \
['click-help-colors>=0.9,<0.10',
 'click>=8.0.1,<9.0.0',
 'cryptocode>=0.1,<0.2',
 'pyfiglet>=0.8.post1,<0.9']

entry_points = \
{'console_scripts': ['prack = passrack:main']}

setup_kwargs = {
    'name': 'passrack',
    'version': '0.1.6',
    'description': "A Command Line Interface to encrypt, decrypt and save passwords. What's new: More exception handling",
    'long_description': "# PassRack- Password Manager\n## `PassRack` : A simple CLI for managing passwords\n\nHave important passwords to store? Use passrack to encrypt your passwords into files and decrypt them whenever you want!\n\n## Install\n\n```\npip3 install passrack \n```\n\n## Dependencies\n+ `click` \n+ `click_help_colors`\n+ `pyfiglet`\n+ `cryptocode`\n\n## Built with\n+ `Python 3.9.5` \n\n## Supported Platforms:\n\n+ Operating System = Cross-Platform\n\n## How to use\n\nOpen powershell for Windows or Terminal for Linux/Mac and  and type ```prack```\n\nIf this result comes, then you have successfully installed rassrack on your system\n\n```\n\n  PassRack: Encrypt, decrypt and save your passwords\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  clear     Clear existing data\n  config    Set your configuration for PassRack\n  decrypt   Decrypt any of your passwords\n  decryptf  Decrypt all your passwords\n  encrypt   Encrypt your message\n  info      Information about PassRack\n  init      Initialize passrack for you to get started with it\n  suggest   Get a password suggestion\n```\n\nelse, try the above steps again!\n\n#### Setup\n\nFirst you need to setup passrack for yourself\n\nProcedure:\n\n- Run `prack init` to initialize prack for your directory\n\nThere should be no output\n\n- Run `prack config -ps <password>` to set your password for prack. It will ask you for your OLD PASSWORD\n  - Now if you haven't configured your passowrd before, enter `fetcher` in the OLD PASSWORD INPUT which is the default password\n\n**NOTE: THIS STORES YOUR PASSWORD FOR PASSRACK AND DOES NOT INDICATE A PASSWORD FOR PASSWORD MANAGEMENT**\n\n- Now you are set up to use passrack\n\n##### Encryption:\n\n```\nprack encrypt {password} {note(optional)}\n```\n\nFor example:\n\n```\nprack encrypt 'Welcome982' -n google\n```\nHere the password `Welcome982` will be stored in encrypted format and stored in your device.\n\nIn the above example, 'google' is an ID that gives the encrypted data and identity.\n\nYou can even use `--note` instead of `-n` to add an ID\n\nGiving an ID is completely optional, but highly recommended for every user. This helps you decrypt your messages easily\n\n##### Decryption\n\nThere are two methods of decrypting/obtaining your passwords\n\n###### SPECIFIC DECRYPTION\n\n```\nprack decrypt -n {note}\n```\n\nFor example:\n\n```\nprack decrypt -n google\n```\n\nThis gives you the stored password identified by `google` NOTE/ID.\n\n###### MASS DECRYPTION\n\n```\nprack decryptf \n```\n\nThis gives you all of your stored passwords\n\n```\nprack decryptf\n```\n\n##### SUGGEST\n\n```\nprack suggest -n google\n```\n\nThis gives a strong password suggestion, also gives you an option to save the password in pm with identifier note.\n\n**NOTE: EVERY DECRYPTION METHOD NEEDS YOUR PassRack PASSWORD, HENCE IF YOU HAVE NOT SETUP PASSRACK, DECRYPTION WONT WORK**\n\n##### CLEAR\n\n`prack clear` cleans the data from data file\n\n## Release Notes\n\n- **Current Release- 0.2.4 (Major Update)**\n\n### What's new?\n\n- Double Encryption makes passwords safe and secure!\n- A beautiful TUI applied\n- Faster Performance\n- The Files are encrypted, and stored in your device, hence it's so secure that even you can't access them without prack\n- Added Password Suggestion\n\n#### Developers\n- [Avanindra Chakraborty](https://github.com/AvanindraC)\n- [Arghya Sarkar](https://github.com/arghyagod-coder)\n- [Shravan Asati](https://github.com/Shravan-1908)\n\n\n### Developer Tools\n\n- [Visual Studio Code](https://github.com/microsoft/vscode)\n\n- [Python 3.9.5](https://python.org)\n\n- [Git](https://git-scm.com)\n\n- [Python Poetry](https://python-poetry.org/)\n\n## License\n\nLicense © 2021-Present Avanindra Chakraborty\n\nThis repository is licensed under the MIT license. See [LICENSE](https://github.com/AvanindraC/PMCLI/blob/main/LICENSE) for details.\n\n## Special Notes\n\n- Contribution is appreciated! \n- If you see anything uncomfortable or not working, file an issue in [the issue page](https://github.com/AvanindraC/PMCLI/issues). Issues aren't ignored by the developers\n- Thanks for seeing my project!",
    'author': 'Avanindra Chakraborty',
    'author_email': 'avanindra.d2.chakraborty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AvanindraC/passrack',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
