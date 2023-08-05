from setuptools import find_packages, setup

setup(
    name="lifeguard-telegram",
    version="0.0.4",
    url="https://github.com/LifeguardSystem/lifeguard-telegram",
    author="Diego Rubin",
    author_email="contact@diegorubin.dev",
    license="GPL2",
    scripts=[],
    include_package_data=True,
    description="Lifeguard integration with Telegram",
    install_requires=["lifeguard", "python-telegram-bot"],
    classifiers=["Development Status :: 3 - Alpha"],
    packages=find_packages(),
)
