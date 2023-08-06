# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickcpp']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['quickcpp = quickcpp.main:main']}

setup_kwargs = {
    'name': 'quickcpp',
    'version': '0.1.1',
    'description': 'Quickly builds a standalone C++ file and runs the result.',
    'long_description': '# quickcpp\n\n`quickcpp` is a small command-line tool to quickly build and run a single C++ file. Handy for quick experimentations.\n\n## Usage\n\nThe simplest usage is `quickcpp <path/to/some/cppfile>`. When called like this, `quickcpp` builds the file (producing a `a.out` file) and runs the result.\n\n```\n$ cat examples/helloworld.cpp \n#include <iostream>\n\nint main(int argc, char** argv) {\n    std::cout << "Hello world!\\n";\n    return 0;\n}\n\n$ quickcpp examples/helloworld.cpp \n- Building ---------------------\nc++ examples/helloworld.cpp -Wall -fPIC -std=c++17 -g\n- Running ----------------------\nHello world!\n```\n\n### Using other libraries\n\nWant to experiment something with [QtWidgets][]? You can specify any installed pkg-config compliant packages using `-p <package>`:\n\n[QtWidgets]: https://doc.qt.io/qt-5.15/qtwidgets-index.html\n\n```\n$ cat examples/qt.cpp \n#include <QApplication>\n#include <QMainWindow>\n\nint main(int argc, char** argv) {\n    QApplication app(argc, argv);\n\n    QMainWindow window;\n    window.setWindowTitle("Hello World");\n    window.show();\n\n    return app.exec();\n}\n\n$ quickcpp -p Qt5Widgets examples/qt.cpp \n- Building ---------------------\nc++ examples/qt.cpp -Wall -fPIC -std=c++17 -g -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_CORE_LIB -I/usr/include/x86_64-linux-gnu/qt5/QtWidgets -I/usr/include/x86_64-linux-gnu/qt5 -I/usr/include/x86_64-linux-gnu/qt5/QtGui -I/usr/include/x86_64-linux-gnu/qt5 -I/usr/include/x86_64-linux-gnu/qt5/QtCore -I/usr/include/x86_64-linux-gnu/qt5 -lQt5Widgets -lQt5Gui -lQt5Core\n- Running ----------------------\n```\n\nYou should see a window like this one:\n\n![qt.png](examples/qt.png)\n\nAny package listed by `pkg-config --list-all` can be used by `quickcpp`.\n\n### Live reload\n\n`quickcpp` can use [entr](http://entrproject.org/) to automatically rebuild and rerun your file. Just install `entr` and run `quickcpp` with the `-l` flag.\n\n## Installation\n\nThe recommended solution is to use [pipx][]:\n\n```\npipx install quickcpp\n```\n\n[pipx]: https://github.com/pipxproject/pipx\n\nBut you can also install it with `pip`:\n\n```\npip install --user quickcpp\n```\n\n## License\n\nApache 2.0\n',
    'author': 'Aurélien Gâteau',
    'author_email': 'mail@agateau.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agateau/quickcpp',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
