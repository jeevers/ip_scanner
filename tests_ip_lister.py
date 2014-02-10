'''
Tests for storage_ip_lister
'''

from sh import date

def test_sh_date():
    '''Some lame test that nose can pick up.'''
    date_out = date()
    assert date_out.exit_code == 0

