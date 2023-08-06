from distutils.core import setup

setup(
      name="easyPyMySQL",
      version="1.62",
      description="简单易用的数据库ORM模块",
      url='https://github.com/AkiYama-Ryou/easyPyMySQL',
      author="ChenRuohan",
      author_email='crh51306@gmail.com',
      packages= ['easyPyMySQL'],

      )
# py -m twine upload dist/*