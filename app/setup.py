from setuptools import setup

setup(name='power_market',
      version='0.5',
      description='Green economical strategy',
      url='https://github.com/Zeryoshka/first_course-work',
      author='Zeryoshka, Irvus',
      author_email='saloshkarev@edu.hse.ru, iatarasenko@edu.hse.ru',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: GPL',  # hz
          'Programming Language :: Python :: 3 :: Only'
      ],
      python_requires='>=3.6, <4',
      install_requires=['datetime', 'csv', 'os', 'flask', 'functools', 'json'],
      entry_points={
          'console_scripts': [
              'powermarket = first_course-work.run-debug.py'
          ]
      }

      )
