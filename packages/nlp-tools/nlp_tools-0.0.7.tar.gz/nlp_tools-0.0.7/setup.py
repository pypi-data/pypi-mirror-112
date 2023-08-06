import codecs
import os
import pathlib
import re

from setuptools import find_packages, setup




__name__ = 'nlp_tools'
__author__ = "fanfanfeng"
__copyright__ = "Copyright 2020, fanfanfeng"
__credits__ = []
__license__ = "Apache License 2.0"
__maintainer__ = "fanfanfeng"
__email__ = "544855237@qq.com"
__url__ = 'https://github.com/BrikerMan/Kashgari'
__description__ = '参考Kashgari项目，然后会扩充一些自己做的项目'

__version__ = '1.0.1'
README = __description__

#with codecs.open('requirements.txt', 'r', 'utf8') as reader:
#    install_requires = list(map(lambda x: x.strip(), reader.readlines()))
install_requires = []

# setup(
#     name=__name__,
#     version=__version__,
#     description=__description__,
#     python_requires='>3.6',
#     long_description=README,
#     long_description_content_type="text/markdown",
#     author=__author__,
#     author_email=__email__,
#     url=__url__,
#     packages=find_packages(exclude=('tests',)),
#     install_requires=install_requires,
#     include_package_data=True,
#     zip_safe=True
#     #license=LGPL,
#
# )

setup(
    name="nlp_tools",
    version='0.0.7',
    description='工程提取字段相关的一些定义以及一些常用函数封装',
    author='qiufengfeng',
    install_requires = [],
    author_email='544855237@qq.com',
    package_dir={'nlp_tools': 'nlp_tools'},
    packages=find_packages(),
    include_package_data=True,
    #package_data={'infoprocessor': ['data/*']},
    license='LGPL',
    zip_safe=False
)


