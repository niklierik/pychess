from setuptools import setup


setup(
    name="PyChess",
    version="1.0",
    description="A GUI chess written in Python.",
    author="Nikli Erik",
    author_email="erik200203@gmail.com",
    url="https://github.com/niklierik/pychess",
    packages=["actors", "scenes", "ai", "assets", "game", "stockfish_versions"],
    py_modules=["main", "__main__"],
    install_requires=["pygame", "chess", "pylint"],
    include_package_data=True,
)
