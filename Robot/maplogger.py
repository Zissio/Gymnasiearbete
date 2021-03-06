import queue
import threading
import socket
import json
import time

_mapfile = None
_data = queue.Queue()
_s = None
_connection = False
_running = False
_conn = None
_addr = None
_done = False

def _handle_connection():
    global _s
    global _connection
    global _conn
    global _addr

    _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _s.bind(("", 1234))
    _s.listen(1)
    try:
        _conn, _addr = _s.accept()
    except:
        return
    print("Anslutning från {}:1234".format(_addr[0]))
    _connection = True

def _handle_data():
    global _running
    global _data
    global _connection
    global _mapfile
    global _conn
    global _addr
    global _done

    _done = False
    while _running:
        position = []
        walls = []
        heading = None

        while not _data.empty():
            d = _data.get(timeout=0.5)
            if "walls" in d:
                walls += d["walls"]
            if "position" in d:
                position += d["position"]
            if "heading" in d:
                heading = d["heading"]

        data = {}
        if len(walls) > 0:
            data["walls"] = walls
        if len(position) > 0:
            data["position"] = position
        if not heading is None:
            data["heading"] = heading

        if len(walls) > 0 or len(position) > 0 or not heading is None:
            if not _mapfile is None and not _mapfile.closed:
                for wall in walls:
                    print("{},{}".format(wall[0], wall[1]), file=_mapfile)

            if _connection:
                try:
                    _conn.sendall(json.dumps(data).encode("utf-8"))
                except:
                    _conn.close()
                    _s.close()
                    _connection = False
                    print("Förlorade anslutning till {}".format(_addr[0]))
    _done = True

def initialize(file=None):
    global _mapfile
    global _running

    _running = True
    if not file is None:
        _mapfile = open(file, "w")
    t = threading.Thread(target=_handle_connection)
    t.setDaemon(True)
    t.start()
    threading.Thread(target=_handle_data).start()

def close():
    global _connection
    global _conn
    global _mapfile
    global _data
    global _running
    global _done

    _running = False
    while not _done:
        pass
    if _connection:
        _conn.close()
    _s.close()
    if not _mapfile is None:
        _mapfile.close()
        _mapfile = None
    _connection = False

def log(**data):
    _data.put(data)