#!/bin/bash

mv hashbuster.py hashbuster
chmod +x hashbuster
sudo mv hashbuster /bin/

if [ $(command -v hashbuster) ]; then
    echo "Hash Buster has been installed."
else
    echo "Installation failed."
fi
