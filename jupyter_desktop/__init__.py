import os
import shlex
from shutil import which
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    vnc_command = ' '.join(shlex.quote(p) for p in [
        '/software/jupyter/tigervnc/1.10.0/usr/bin/vncserver',
        '-rfbunixpath', sockets_path,
        '-xstartup', '/software/jupyter/jupyter-remote-desktop-proxy/jupyter_desktop/share/xstartup',
        '-SecurityTypes', 'None',
        '-verbose',
        '-fg',
    ])

    return {
        'command': [
            'websockify', '-v',
            '--web', '/software/jupyter/novnc',
            '--heartbeat', '30',
            '--unix-target', sockets_path,
            '{port}',
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}; rm -rf {sockets_dir}'
        ],
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True
    }
