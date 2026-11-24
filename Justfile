env:=['powershell.exe']


build:
    docker compose up -d --build

test suite='all':
    pytest -n auto --loadscope dist
