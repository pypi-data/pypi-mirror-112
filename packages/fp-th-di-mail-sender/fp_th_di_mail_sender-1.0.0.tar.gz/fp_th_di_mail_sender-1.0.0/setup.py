from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fp_th_di_mail_sender',
    packages=find_packages(include=['fp_th_di_mail_sender']),
    version='1.0.0',
    description='Foodpanda Thailand Data & Insight team - Utility function for mail sending using SMTP',
    author='Mathara Rojanamontien',
    author_email="mathara.rojanamontien@foodpanda.co.th",
    license='Delivery Hero (Thailand) Co., Ltd.',
    install_requires=[ ],
    long_description=long_description,
)