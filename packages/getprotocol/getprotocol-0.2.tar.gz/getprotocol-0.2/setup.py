from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read().strip()

setup(name='getprotocol',
	version='0.2',
	description='Simple script to get if host is using http or https.',
	long_description=long_description,
	long_description_content_type='text/markdown',  # This is important!
	url='https://github.com/Anon-Exploiter/getprotocol',
	author='Syed Umar Arfeen',
	author_email='18597330+Anon-Exploiter@users.noreply.github.com',
	license='MIT',
	packages=find_packages(),
	install_requires=[
		'requests',
	],
	entry_points={
		'console_scripts': [
			'getprotocol = getprotocol.getprotocol:main'
		],
	},
	zip_safe=False
)