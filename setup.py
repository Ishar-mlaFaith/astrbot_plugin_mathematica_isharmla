from setuptools import setup


def parse_requirements(fn):
    with open(fn) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


setup(
    # 基础元数据
    name="astrbot_plugin_mathematica_isharmla",
    version="1.0.0",
    author="Ishar-mlaFaith",
    author_email="206766382@qq.com",
    description="尝试实现让astrbot使用mma",
    url="https://github.com/Ishar-mlaFaith/astrbot_plugin_mathematica_isharmla",

    # 依赖
    install_requires=parse_requirements("requirements.txt")
)