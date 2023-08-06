import os
KPS_ENDPOINT = os.getenv('KPS_ENDPOINT', 'https://test.ntnxsherlock.com')
USER_ID = os.getenv('KPS_USER_ID', 'e3edb397-3322-4e68-bd5e-436a31185fd2')
# The user email and password will be read from build environment
USER_EMAIL = os.getenv('KPS_USER_EMAIL', "test@ntnxsherlock.com")
USER_PWD = os.getenv('KPS_PWD', '<pwd>')
NUTANIX_EMAIL = os.getenv('NUTANIX_EMAIL', 'sameeksha.chepe@nutanix.com')
NUTANIX_USER_NAME = os.getenv('NUTANIX_USER_NAME','sameeksha.chepe')

