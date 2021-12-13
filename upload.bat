del "dist" /s /f /q
rd "dist" /s /q
del /s /f /q "src/win32_bridge.egg-info"
rd /s /q "src/win32_bridge.egg-info"
del /s /f /q "win32-bridge-*"

python -m pip install --upgrade build
python -m build
python -m pip install --upgrade twine
twine upload -r pypi dist/*
