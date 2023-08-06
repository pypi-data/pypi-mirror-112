from distutils.core import setup
setup(
  name = 'dave_db_utils',         # How you named your package folder (MyLib)
  packages = ['dave_db_utils'],   # Chose the same as "name"
  version = '0.13',      # Start with a small number and increase it with every change you make
  license='agpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Utilities to help work with Databricks',   # Give a short description about your library
  author = 'David Levy',                   # Type in your name
  author_email = 'david.g.levy@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/davidglevy/dave-db-utils',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/davidglevy/dave-db-utils/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['UTILITY', 'DATABRICKS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'py4j'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)