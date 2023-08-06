from distutils.core import setup
setup(
  name='pyrraform',
  packages=['pyrraform'],
  version='0.0',
  license='MIT',
  description='Terraform Wrapper',
  author='Cedric Menec',
  author_email = 'cedric.menec@gmail.com',
  url='https://github.com/cedricmenec/pyrraform',
  download_url='',    # I explain this later on
  keywords = ['terraform', 'wrapper'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)