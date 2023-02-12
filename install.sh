#!/bin/bash

pip install argparse
pip install colorama
pip install hashlib
pip install hashid

mv hashbuster.py hashbuster
chmod +x hashbuster
sudo mv hashbuster /bin/

if [ $(command -v hashbuster) ]; then
    echo "Hash Buster has been installed."
else
    echo "Installation failed."
fi
