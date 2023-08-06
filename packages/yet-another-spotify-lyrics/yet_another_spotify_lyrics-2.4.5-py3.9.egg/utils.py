import os
import re
import select
import sys
import termios
import urllib.parse
import fcntl
import errno
import struct
from subprocess import Popen, PIPE

import dbus
import requests
from bs4 import BeautifulSoup


W3MIMGDISPLAY_ENV = "W3MIMGDISPLAY_PATH"
W3MIMGDISPLAY_OPTIONS = []
W3MIMGDISPLAY_PATHS = [
    # '/home/goktug/test/w3mimg/w3m/w3mimgdisplay',
    '/usr/lib/w3m/w3mimgdisplay',
    # '/usr/libexec/w3m/w3mimgdisplay',
    # '/usr/lib64/w3m/w3mimgdisplay',
    # '/usr/libexec64/w3m/w3mimgdisplay',
    # '/usr/local/libexec/w3m/w3mimgdisplay',
]


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def move_cursor(x, y):
    sys.stdout.write(f"\033[{y};{x}H")

def delete_line():
    sys.stdout.write('\x1b[2K')

def boldify(string):
    return f'\033[1m{string}\033[0m'

def fetch_lyrics(artist, title):
    title = re.sub(r'[-\*"]', ' ', title)
    search_string = f'{artist} {title} lyrics'
    search_string = urllib.parse.quote_plus(search_string)
    url = 'https://google.com/search?q=' + search_string
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml", from_encoding='UTF-8')
    raw_lyrics = (soup.findAll('div', attrs={'class': 'hwc'}))
    final_lyrics = str.join(u'\n', map(str, raw_lyrics))
    final_lyrics = re.sub(r'<(.*)>', '', string=final_lyrics)
    final_lyrics = '\n'.join(final_lyrics.split('\n')[:-2])
    return final_lyrics

def terminal_size():
    rows, columns = map(int, os.popen('stty size', 'r').read().split())
    return rows, columns

class KeyPoller():
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self, timeout=0.0):
        dr,dw,de = select.select([sys.stdin], [], [], timeout)
        return sys.stdin.read(1) if not dr == [] else None

    def flush(self):
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class Spotify(object):
    def __init__(self):
        session_bus = dbus.SessionBus()
        try:
            self.spotify_bus = session_bus.get_object(
                "org.mpris.MediaPlayer2.spotify",
                "/org/mpris/MediaPlayer2")
        except dbus.exceptions.DBusException:
            sys.exit("Can't access to Spotify DBUS")
        self.player_interface = dbus.Interface(
            self.spotify_bus, dbus_interface='org.mpris.MediaPlayer2.Player')
        self.properties_interface = dbus.Interface(
            self.spotify_bus, "org.freedesktop.DBus.Properties")

    def metadata(self):
        metadata = self.properties_interface.Get(
            "org.mpris.MediaPlayer2.Player", "Metadata")
        title = metadata['xesam:title'].replace("&", "&amp;")
        artist = metadata['xesam:artist'][0].replace("&", "&amp;")
        album = metadata['xesam:album'].replace("&", "&amp;")
        art_url = f"https://i.scdn.co/image/{metadata['mpris:artUrl'].replace('&', '&amp;').split('/')[-1]}"
        return title, artist, album, art_url

    def next(self):
        self.player_interface.Next()

    def prev(self):
        self.player_interface.Previous()

    def toggle(self):
        self.player_interface.PlayPause()

def print_help():
    print(boldify('''
| Action              | Keybinding    |
|:-------------------:|:-------------:|
| Scroll Up           |      k        |
| Scroll Down         |      j        |
| Beginning of Lyrics |      gg       |
| End of Lyrics       |      G        |
| Edit Lyrics         |      e        |
| Refresh             |      r        |
| Toggle              |      t        |
| Next                |      n        |
| Prev                |      p        |
| Update Lyrics       |      d        |
| Toggle Album Cover  |      i        |
| Help                |      h        |
| Quit Program        |      q        |

- Edit Lyrics: Open lyrics in `$EDITOR`.
- Refresh: Refresh lyrics and song metadata.
- Toggle: Play or Pause currently playing song.
- Next: Play next song.
- Prev: Play previous song.
- Update Lyrics: Deletes cached lyrics and fetches lyrics from the internet.
- Help: Show keybindings 5 seconds.'''))


# Adapted from
# https://github.com/ranger/ranger/blob/a53f056cb2d9586ed97c7757a1e49d30d873c27d/ranger/ext/img_display.py
class ImageDisplayError(Exception):
    pass


class ImgDisplayUnsupportedException(Exception):
    pass


class W3MImageDisplayer():
    is_initialized = False
    working_dir = os.environ.get('XDG_RUNTIME_DIR', os.path.expanduser("~") or None)

    def __init__(self):
        self.binary_path = None
        self.process = None

    def initialize(self):
        """start w3mimgdisplay"""
        self.binary_path = None
        self.binary_path = self._find_w3mimgdisplay_executable()  # may crash
        self.process = Popen([self.binary_path] + W3MIMGDISPLAY_OPTIONS, cwd=self.working_dir,
                             stdin=PIPE, stdout=PIPE, universal_newlines=True)
        self.is_initialized = True

    @staticmethod
    def _find_w3mimgdisplay_executable():
        paths = [os.environ.get(W3MIMGDISPLAY_ENV, None)] + W3MIMGDISPLAY_PATHS
        for path in paths:
            if path is not None and os.path.exists(path):
                return path
        raise ImageDisplayError("No w3mimgdisplay executable found.  Please set "
                                "the path manually by setting the %s environment variable.  (see "
                                "man page)" % W3MIMGDISPLAY_ENV)

    def _get_font_dimensions(self):
        # Get the height and width of a character displayed in the terminal in
        # pixels.
        if self.binary_path is None:
            self.binary_path = self._find_w3mimgdisplay_executable()
        farg = struct.pack("HHHH", 0, 0, 0, 0)
        fd_stdout = sys.stdout.fileno()
        fretint = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, farg)
        rows, cols, xpixels, ypixels = struct.unpack("HHHH", fretint)
        if xpixels == 0 and ypixels == 0:
            process = Popen([self.binary_path, "-test"], stdout=PIPE, universal_newlines=True)
            output, _ = process.communicate()
            output = output.split()
            xpixels, ypixels = int(output[0]), int(output[1])
            # adjust for misplacement
            xpixels += 2
            ypixels += 2

        return (xpixels // cols), (ypixels // rows)

    def draw(self, path, start_x, start_y, width, height):
        if not self.is_initialized or self.process.poll() is not None:
            self.initialize()
        input_gen = self._generate_w3m_input(path, start_x, start_y, width,
                                             height)

        self.process.stdin.write(input_gen)
        self.process.stdin.flush()
        self.process.stdout.readline()
        # self.quit()
        # self.is_initialized = False

    def clear(self, start_x, start_y, width, height):
        if not self.is_initialized or self.process.poll() is not None:
            self.initialize()

        fontw, fonth = self._get_font_dimensions()

        cmd = "6;{x};{y};{w};{h}\n4;\n3;\n".format(
            x=int((start_x - 0.2) * fontw),
            y=start_y * fonth,
            # y = int((start_y + 1) * fonth), # (for tmux top status bar)
            w=int((width + 0.4) * fontw),
            h=height * fonth + 1,
            # h = (height - 1) * fonth + 1, # (for tmux top status bar)
        )

        self.process.stdin.flush()
        self.process.stdout.readline()

    def _generate_w3m_input(self, path, start_x, start_y, max_width, max_height):
        """Prepare the input string for w3mimgpreview
        start_x, start_y, max_height and max_width specify the drawing area.
        They are expressed in number of characters.
        """
        fontw, fonth = self._get_font_dimensions()
        if fontw == 0 or fonth == 0:
            raise ImgDisplayUnsupportedException

        max_width_pixels = max_width * fontw
        max_height_pixels = max_height * fonth - 2
        # (for tmux top status bar)
        # max_height_pixels = (max_height - 1) * fonth - 2

        # get image size
        cmd = "5;{path}\n".format(path=path)

        self.process.stdin.write(cmd)
        self.process.stdin.flush()
        output = self.process.stdout.readline().split()

        if len(output) != 2:
            raise ImageDisplayError('Failed to execute w3mimgdisplay', output)

        width = int(output[0])
        height = int(output[1])

        # get the maximum image size preserving ratio
        if width > max_width_pixels:
            height = (height * max_width_pixels) // width
            width = max_width_pixels
        if height > max_height_pixels:
            width = (width * max_height_pixels) // height
            height = max_height_pixels

        return "0;1;{x};{y};{w};{h};;;;;{filename}\n4;\n3;\n".format(
            x=start_x,
            y=start_y,
            # y = (start_y + 1) * fonth, # (for tmux top status bar)
            w=width,
            h=height,
            filename=path,
        )

    def quit(self):
        if self.is_initialized and self.process and self.process.poll() is None:
            self.process.kill()
