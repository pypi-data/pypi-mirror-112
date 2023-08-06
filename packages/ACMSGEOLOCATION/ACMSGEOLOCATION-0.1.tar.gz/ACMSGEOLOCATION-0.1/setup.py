from distutils.core import setup
setup(
  name = 'ACMSGEOLOCATION',         # How you named your package folder (MyLib)
  packages = ['ACMSGEOLOCATION'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package will provide the accurate GPS location of your mobile. It is mandatory to connect your system and phone with same network and use IP WebCam App to find the url.',   # Give a short description about your library
  author = 'ABHISHEK MISHRA',                   # Type in your name
  author_email = 'mishraabhi8924@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Abhishekmishra-17/ACMSGEOLOCATION',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Abhishekmishra-17/ACMSGEOLOCATION/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['GPS','geolocation','IP WebCam','mobile data','location'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Pillow',
          'twilio',
          'selenium',
          'pytesseract',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',#Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    
  ],
)
