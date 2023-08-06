from distutils.core import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name = 'shrtcode-py',         # How you named your package folder (MyLib)
  packages = ['shrtcode-py'],   # Chose the same as "name"
  version = '1.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for shrtco.de API',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'tailsjs',                   # Type in your name
  author_email = 'tjs@retard.yo',      # Type in your E-Mail
  url = 'https://github.com/tailsjs/shrtco.de-py',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/tailsjs/shrtco.de-py/archive/refs/tags/1.0.tar.gz',    # I explain this later on
  keywords = ["shrtco.de","short","url","api","shorter","emoji","password","pass"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
          'urllib3',
          'requests_toolbelt'
      ],
    classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)