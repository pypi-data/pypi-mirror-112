from distutils.core import setup
from setuptools import find_packages

setup(name='stduino',  # 包名
      version='0.0.3',  # 版本号
      description='Stduino IDE For win、mac、linux',
      long_description='Stduino IDE For Global',
      author='文涛',
      author_email='33672008@qq.com',
      url='http://www.stduino.com',
      license='',#'pyqtwebengine>=5.15',
      install_requires=['pyserial>=2.0','pyqt5>=5.15','pywebview>=3.0','requests>=2.20','qdarkstyle==2.8.1','pygdbmi>=0.10','qscintilla>=2.10','watchdog>=2.1'],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities'
      ],
      keywords='Stduino IDE',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
