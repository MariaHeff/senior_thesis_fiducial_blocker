from setuptools import find_packages, setup

package_name = 'fiducial_blocker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/fiducial_blocker/launch', ['launch/fiducial_blocker_launch.py']),
    ],
    include_package_data=True,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jetson-orin-spot',
    maintainer_email='jetson-orin-spot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		'detect_fiducials = fiducial_blocker.detect_fiducials:main',
		'fiducial_filter_frontright = fiducial_blocker.filter_frontright:main',
		'fiducial_filter_frontleft = fiducial_blocker.filter_frontleft:main',
		'fiducial_filter_right = fiducial_blocker.filter_right:main',
		'fiducial_filter_left = fiducial_blocker.filter_left:main',
		'fiducial_filter_back = fiducial_blocker.filter_back:main',
		'body_obstacle = fiducial_blocker.body_obstacle:main',
		
        ],
    },
)
