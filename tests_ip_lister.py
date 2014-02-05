from sh import date

def test_sh_date():
        date_out = date()
        assert date_out.exit_code == 0
