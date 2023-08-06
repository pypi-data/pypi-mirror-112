from __future__ import print_function

from setuptools import setup, find_packages




setup(
    name="ext_time",
    version="1.1.1",
    author="sunny_shm",
    author_email="1576396251@qq.com",
    description="shm-时间解析",
    long_description=open("README.txt", encoding="utf8").read(),
    url="https://www.baidu.com/",
    packages=find_packages(),
    # package_data={
    #     "zlparse.parse_diqu": ['list.json', 'list2.json'],
    #     "zlparse.parse_time": ['quyu_time_func.json','Readme.txt'],
    #     "zlparse.parse_project_code": ['patterns.json'],
    #     "zlparse.zlshenpi": ['shenpi_func.json'],
    #     "zlparse.zlparse_page.core": ['words.txt'],
    #     "zlparse.zlparse_page_many.core": ['words.txt'],
    #     "zlparse.zlparse_page": ['need.json','needless.json'],
    #     "zlparse.zlparse_page_many": ['need.json', 'needless.json'],
    #     "zlparse.parse_lx": ['zhaobiao_need.json', 'zhongbiao_need.json','feibiao_need.json','zishen_need.json','biangeng_need.json','dayi_need.json'],
    #     "zlparse.parse_ggname_sub": ['zhaobiao_need_xmmc.json', 'zhongbiao_need_xmmc.json', 'feibiao_need_xmmc.json', 'zishen_need_xmmc.json', 'biangeng_need_xmmc.json', 'dayi_need_xmmc.json','common_need.json'],
    #     "zlparse.parse_hy": ['list_hy.json']
    # },

    # install_requires=[
    #     "jieba",
    #     "beautifulsoup4>=4.6.3",
    #     "lmfscrap>=1.1.0",
    #     "lmf>=2.1.6",
    # ],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.5"
    ],
)
