#!/usr/bin/env python
from bodil import app, BODIL_PORT, BODIL_DEBUG

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=BODIL_PORT, debug=BODIL_DEBUG)
