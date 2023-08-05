import setuptools  

with open("README.md", "r", encoding="utf-8") as fh:  
    long_description = fh.read()  

setuptools.setup(  
    name="discord_voice_text",  
    version="0.0.5",  
    author="furimu",  
    description="Discord.py2.0以上でVoice Textを非同期で使えるようにしたもの",  
    long_description=long_description,  
    long_description_content_type="text/markdown",
    install_requires="discord.py>=2.0.0a",
    license="MIT License",
    url="",  
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    classifiers=[  
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",  
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",  
    ],  
)  