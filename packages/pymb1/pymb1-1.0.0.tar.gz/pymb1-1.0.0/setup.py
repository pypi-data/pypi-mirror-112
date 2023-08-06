import setuptools

setuptools.setup(
    name="pymb1",
    version="1.0.0",
    author="reaitten",
    author_email="wsy0xf2u8@relay.firefox.com",
    description="A telegram bot for all your mirror needs",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.8.2",
    url="https://github.com/reaitten/pymb1",
    project_urls={
        "Bug Tracker": "https://github.com/reaitten/pymb1/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',  
        'psutil', 
        'python-telegram-bot==12.6.1', 
        'google-api-python-client>=1.7.11,<1.7.20', 
        'google-auth-httplib2>=0.0.3,<0.1.0', 
        'google-auth-oauthlib>=0.4.1,<0.10.0', 
        'aria2p>=0.9.0,<0.15.0', 
        'python-dotenv>=0.10', 
        'tenacity>=6.0.0', 
        'python-magic', 
        'beautifulsoup4>=4.8.2,<4.8.10', 
        'Pyrogram>=0.16.0,<0.16.10', 
        'TgCrypto>=1.1.1,<1.1.10', 
        'youtube_dl', 
        'megasdkrestclient>=0.1.1,<1.0.0'],
    scripts=['extract'],
    entry_points={
        "console_scripts":[
            "pymb1 = bot.__main__:main"
                ],
    },
)