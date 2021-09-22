import sys
import os
import pytest
from . import subprocess

module_dir = os.path.dirname(__file__)
shellcmd = os.path.join(module_dir, 'shellcmd_test.py')

def stripr(s):
    if type(s) is str:
        return s.replace('\r', '')
    else:
        return s.replace(b'\r', b'')

class TestLogTimeoutOnly:
    def test_logtimeout_only(self):
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-s', '3'], log_timeout=1)
        assert stripr(ex.value.stdout) == b'0 line\n'
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        # float timeout value
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd], log_timeout=0.9)
        assert stripr(ex.value.stdout) == b'0 line\n'
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        # utf-8 encoding 
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd], log_timeout=0.9, text=True,
                           encoding='utf-8', errors='strict')
        assert stripr(ex.value.stdout) == '0 line\n'
        assert stripr(ex.value.stderr) == ''
        assert ex.typename == 'LogTimeoutExpired'

        rc = subprocess.run([sys.executable, shellcmd], log_timeout=3)
        assert rc.returncode == 0
        assert stripr(rc.stdout) == b'0 line\n'
        assert stripr(rc.stderr) == b''


    def test_logtimeout_only_iter(self):
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'], log_timeout=1)
        assert b'0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'], log_timeout=1.4)
        assert b'0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'], log_timeout=1.4,
                            text=True, encoding='utf-8', errors='strict')
        assert '0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == ''
        assert ex.typename == 'LogTimeoutExpired'

        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'], log_timeout=3)
        assert rc.returncode == 0
        assert stripr(rc.stdout) == b'0 line\n1 line\n2 line\n'
        assert stripr(rc.stderr) == b''

        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'], log_timeout=5,
                            text=True, encoding='utf-8', errors='strict')
        assert rc.returncode == 0
        assert stripr(rc.stdout) == '0 line\n1 line\n2 line\n'
        assert stripr(rc.stderr) == ''

class TestTimeoutOnly:
    def test_timeout_only_no_output(self):
        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd], timeout=1)
        assert ex.value.stdout is None
        assert ex.value.stderr is None
        assert ex.typename == 'TimeoutExpired'

        rc = subprocess.run([sys.executable, shellcmd], timeout=2)
        assert rc.returncode == 0


    def test_timeout_only_capture(self):
        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd], timeout=1, capture_output=True)
        assert stripr(ex.value.stdout) == b'0 line\n'
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'TimeoutExpired'

        rc = subprocess.run([sys.executable, shellcmd], timeout=2, capture_output=True)
        assert rc.returncode == 0
        assert stripr(rc.stdout) == b'0 line\n'
        assert stripr(rc.stderr) == b''


    def test_timeout_only_capture_text(self):
        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd], timeout=1, capture_output=True,
                            text=True, encoding='utf-8', errors='strict')
        assert stripr(ex.value.stdout) == '0 line\n'
        assert stripr(ex.value.stderr) == ''
        assert ex.typename == 'TimeoutExpired'

        rc = subprocess.run([sys.executable, shellcmd], timeout=2, capture_output=True,
                            text=True, encoding='utf-8', errors='strict')
        assert rc.returncode == 0
        assert stripr(rc.stdout) == '0 line\n'
        assert stripr(rc.stderr) == ''

class TestTimeoutAndLogTimeout:
    def test_logtimeout_first(self):
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1', '-l', '3', '-o', 'yes'],
                            timeout=10, log_timeout=2)
        assert stripr(ex.value.stdout) == b'0 line\n1 line\n2 line\nlast line\n'
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '2', '-l', '3', '-o', 'yes'],
                            timeout=10, log_timeout=1)
        assert b'0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '2', '-l', '3', '-o', 'yes'],
                            timeout=10, log_timeout=1)
        assert b'0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '2', '-l', '3', '-o', 'yes'],
                            timeout=10, log_timeout=1, text=True,
                            encoding='utf-8', errors='strict')
        assert stripr(ex.value.stdout) == '0 line\n'
        assert stripr(ex.value.stderr) == ''
        assert ex.typename == 'LogTimeoutExpired'

    def test_timeout_first(self):
        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1', '-l', '3', '-o', 'yes'],
                            timeout=4, log_timeout=2)
        assert stripr(ex.value.stdout) == b'0 line\n1 line\n2 line\nlast line\n'
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'TimeoutExpired'

        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1', '-l', '3', '-o', 'yes'],
                            timeout=1, log_timeout=3)
        assert b'0 line\n' in stripr(ex.value.stdout)
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'TimeoutExpired'

class TestNoTimeout:
    def test_timeout_first(self):
        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'])
        assert rc.returncode == 0

        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5'],
                capture_output=True, text=True, encoding='utf-8', errors='strict')
        assert rc.returncode == 0
        assert stripr(rc.stdout) == '0 line\n1 line\n2 line\n'
        assert stripr(rc.stderr) == ''

class TestWithStderr:
    def test_with_stderr(self):
        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5', '-e', 'yes'])
        assert rc.returncode == 0

        rc = subprocess.run([sys.executable, shellcmd, '-c', '3', '-s', '1.5', '-e', 'yes'],
                capture_output=True, text=True, encoding='utf-8', errors='strict')
        assert rc.returncode == 0
        assert stripr(rc.stdout) == '0 line\n2 line\n'
        assert stripr(rc.stderr) == '1 line\n'

class TestNoOutput:
    def test_no_output_log_timeout(self):
        with pytest.raises(subprocess.LogTimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '0', '-o', 'no', '-l', '10'],
                            log_timeout=3)
        assert stripr(ex.value.stdout) == b''
        assert stripr(ex.value.stderr) == b''
        assert ex.typename == 'LogTimeoutExpired'

    def test_no_output_proc_timeout(self):
        with pytest.raises(subprocess.TimeoutExpired) as ex:
            subprocess.run([sys.executable, shellcmd, '-c', '0', '-o', 'no', '-l', '10'],
                            timeout=3, capture_output=True, text=True, encoding='utf-8',
                            errors='strict')
        assert stripr(ex.value.stdout) == ''
        assert stripr(ex.value.stderr) == ''
        assert ex.typename == 'TimeoutExpired'
