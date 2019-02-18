Invoking CMake setup: 'cmake /tmp/pip-build-HqdlWl/dlib/tools/python -DCMAKE_LIBRARY_OUTPUT_DIRECTORY=/tmp/pip-build-HqdlWl/dlib/build/lib.linux-armv7l-2.7 -DPYTHON_EXECUTABLE=/usr/bin/python -DCMAKE_BUILD_TYPE=Release'

Invoking CMake build: 'cmake --build . --config Release -- -j1'

running install_lib

copying build/lib.linux-armv7l-2.7/dlib.so -> /usr/local/lib/python2.7/dist-packages

error: [Errno 13] Permission denied: '/usr/local/lib/python2.7/dist-packages/dlib.so'

----------------------------------------
Cleaning up...
Command /usr/bin/python -c "import setuptools, tokenize;__file__='/tmp/pip-build-HqdlWl/dlib/setup.py';exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\r\n', '\n'), __file__, 'exec'))" install --record /tmp/pip-WhQlEw-record/install-record.txt --single-version-externally-managed --compile failed with error code 1 in /tmp/pip-build-HqdlWl/dlib
Storing debug log for failure in /home/pi/.pip/pip.log

