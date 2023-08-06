"""Uploaded data to nuuuwan/elections_lk:data branch."""

import os


def upload_data():
    """Upload data."""
    os.system('echo "test data" > /tmp/elections_lk.test.txt')
    os.system('echo "# elections_lk" > /tmp/README.md')


if __name__ == '__main__':
    upload_data()
