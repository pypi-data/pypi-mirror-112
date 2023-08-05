from setuptools import setup


VERSION = "1.4.1"


with open("README.md") as f:
    readme = f.read()


setup(
    name="sylo",
    version=VERSION,
    description="SYLO Python Pomodoro Timer",
    long_description=readme,
    long_description_content_type="text/markdown",  # This is important!
    url="http://github.com/rob-parker-what/sylo",
    author="rob-parker-what",
    author_email="robparkerwhat.dev@gmail.com",
    license="MIT",
    packages=["sylo"],
    entry_points={
        "console_scripts": ["sylo=sylo.cmdline:main"],
    },
    install_requires=[
        "colorama==0.4.4",
        "simpleaudio==1.0.4",
        "beepy==1.0.7",
        "tqdm==4.61.1",
        "pytimedinput==1.3.1",
        "pyfiglet==0.8.post1",
        "pandas==1.1.5",
        "termgraph==0.5.1",
    ],
    package_data={"sylo": ["data"]},
    zip_safe=False,
    python_requires=">=3.7",
    keywords="pomodoro tomato timer terminal pomodoro-timer",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
