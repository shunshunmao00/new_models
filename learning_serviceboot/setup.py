# -*- coding: utf-8 -*-
# ===============LICENSE_START=======================================================
# Acumos Apache-2.0
# ===================================================================================
# Copyright (C) 2017-2018 AT&T Intellectual Property & Tech Mahindra. All rights reserved.
# ===================================================================================
# This Acumos software file is distributed by AT&T and Tech Mahindra
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================
from setuptools import setup, find_packages


with open("README.md", "r", encoding='utf-8') as file:
    long_description = file.read()


setup(
    name='cubeai_model_runner',
    version='2.3.1',
    author='cubeai',
    author_email='cubeai@163.com',
    description='CubeAI模型运行器',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'cython==0.29.21',
        'requests==2.24.0',
        'tornado==6.0.4',
        'pyyaml==5.3.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points="""
    [console_scripts]
    cubeai_model_runner=cubeai_model_runner.cubeai_model_runner:start
    cubeai_model_pack=cubeai_model_runner.cubeai_model_pack:pack_model
    cubeai_model_pack_bin=cubeai_model_runner.cubeai_model_pack:pack_model_bin
    """,
    keywords='CubeAI machine learning model runner server ml ai',
    python_requires='>=3.5',
    url='https://github.com/cube-ai/cubeai-model-runner.git',
)
