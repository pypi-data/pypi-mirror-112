# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

packages = \
['lib']

package_data = \
{'': ['*']}

modules = \
['__init__']
install_requires = \
['Pillow>=8.3.0,<9.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'robotframework>=4.0.3,<5.0.0']

entry_points = \
{'console_scripts': ['carrot-executor = carrot_executor:main']}

setup_kwargs = {
    'name': 'carrot-executor',
    'version': '0.6.4',
    'description': 'Camunda external task Robot Framework execution scheduler',
    'long_description': 'Camunda external task Robot Framework execution scheduler\n=========================================================\n\n**Technology preview.**\n\n`carrot-executor` is an opinionated decoupled Camunda external task executor concept for scheduling Robot Framework RPA tasks. The concept separates task locking from the execution scheduling.\n\n[![](https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgQ2Fycm90XG4gICAgcGFydGljaXBhbnQgRXhlY3V0b3JcbiAgICBwYXJ0aWNpcGFudCBSb2JvdFxuXG4gICAgQ2Fycm90LT4-Q2FtdW5kYTogRmV0Y2ggYW5kIGxvY2tcbiAgICBsb29wXG4gICAgQ2FtdW5kYS0tPj5DYXJyb3Q6IFRhc2tcbiAgICBwYXJcbiAgICBDYXJyb3QtPj4rRXhlY3V0b3I6IFNjaGVkdWxlXG4gICAgRXhlY3V0b3ItPj4rUm9ib3Q6IEV4ZWN1dGVcbiAgICBwYXJcbiAgICBsb29wXG4gICAgUm9ib3QtPj5DYW11bmRhOiBHZXQgdGFzayB2YXJpYWJsZVxuICAgIENhbXVuZGEtLT4-Um9ib3Q6IFZhcmlhYmxlIHZhbHVlXG4gICAgZW5kXG4gICAgZW5kXG4gICAgcGFyXG4gICAgbG9vcFxuICAgIFJvYm90LT4-Q2FtdW5kYTogU2V0IHRhc2sgdmFyaWFibGVcbiAgICBlbmRcbiAgICBlbmRcbiAgICBhbHRcbiAgICBSb2JvdC0-PkNhbXVuZGE6IENvbXBsZXRlIHRhc2tcbiAgICBlbmRcbiAgICBhbHRcbiAgICBSb2JvdC0-PkNhbXVuZGE6IEhhbmRsZSBmYWlsdXJlXG4gICAgZW5kXG4gICAgYWx0XG4gICAgUm9ib3QtPj5DYW11bmRhOiBIYW5kbGUgQlBNTiBlcnJvXG4gICAgZW5kXG4gICAgUm9ib3QtLT4-LUV4ZWN1dG9yOiBbZXhpdCBjb2RlXVxuICAgIGVuZFxuICAgIHBhclxuICAgIGxvb3AgXG4gICAgQ2Fycm90LT4-RXhlY3V0b3I6IFBvbGwgc3RhdHVzXG4gICAgYWx0XG4gICAgRXhlY3V0b3ItLT4-Q2Fycm90OiBbcGVuZGluZ11cbiAgICBDYXJyb3QtPj5DYW11bmRhOiBFeHRlbmQgbG9ja1xuICAgIGVuZFxuICAgIGFsdFxuICAgIEV4ZWN1dG9yLS0-Pi1DYXJyb3Q6IFtjb21wbGV0ZWRdXG4gICAgZW5kXG4gICAgZW5kXG4gICAgZW5kXG4gICAgZW5kIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZSwiYXV0b1N5bmMiOnRydWUsInVwZGF0ZURpYWdyYW0iOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/edit/##eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgQ2Fycm90XG4gICAgcGFydGljaXBhbnQgRXhlY3V0b3JcbiAgICBwYXJ0aWNpcGFudCBSb2JvdFxuXG4gICAgQ2Fycm90LT4-Q2FtdW5kYTogRmV0Y2ggYW5kIGxvY2tcbiAgICBsb29wXG4gICAgQ2FtdW5kYS0tPj5DYXJyb3Q6IFRhc2tcbiAgICBwYXJcbiAgICBDYXJyb3QtPj4rRXhlY3V0b3I6IFNjaGVkdWxlXG4gICAgRXhlY3V0b3ItPj4rUm9ib3Q6IEV4ZWN1dGVcbiAgICBwYXJcbiAgICBsb29wXG4gICAgUm9ib3QtPj5DYW11bmRhOiBHZXQgdGFzayB2YXJpYWJsZVxuICAgIENhbXVuZGEtLT4-Um9ib3Q6IFZhcmlhYmxlIHZhbHVlXG4gICAgZW5kXG4gICAgZW5kXG4gICAgcGFyXG4gICAgbG9vcFxuICAgIFJvYm90LT4-Q2FtdW5kYTogU2V0IHRhc2sgdmFyaWFibGVcbiAgICBlbmRcbiAgICBlbmRcbiAgICBhbHRcbiAgICBSb2JvdC0-PkNhbXVuZGE6IENvbXBsZXRlIHRhc2tcbiAgICBlbmRcbiAgICBhbHRcbiAgICBSb2JvdC0-PkNhbXVuZGE6IEhhbmRsZSBmYWlsdXJlXG4gICAgZW5kXG4gICAgYWx0XG4gICAgUm9ib3QtPj5DYW11bmRhOiBIYW5kbGUgQlBNTiBlcnJvXG4gICAgZW5kXG4gICAgUm9ib3QtLT4-LUV4ZWN1dG9yOiBbZXhpdCBjb2RlXVxuICAgIGVuZFxuICAgIFxuICAgIGxvb3AgXG4gICAgQ2Fycm90LT4-RXhlY3V0b3I6IFBvbGwgc3RhdHVzXG4gICAgYWx0XG4gICAgRXhlY3V0b3ItLT4-Q2Fycm90OiBbcGVuZGluZ11cbiAgICBDYXJyb3QtPj5DYW11bmRhOiBFeHRlbmQgbG9ja1xuICAgIGVuZFxuICAgIGFsdFxuICAgIEV4ZWN1dG9yLS0-Pi1DYXJyb3Q6IFtjb21wbGV0ZWRdXG4gICAgZW5kXG4gICAgZW5kXG4gICAgZW5kIiwibWVybWFpZCI6IntcbiAgXCJ0aGVtZVwiOiBcImRlZmF1bHRcIlxufSIsInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)\n\nIn this concept, Carrot external task client, based on [camunda-external-task-client-js](https://github.com/camunda/camunda-external-task-client-js) fetches configured external tasks from Camunda, schedules their execution, and keeps the tasks locked at Camunda until their executor has been completed. The Carrot external task client only completes task (by creating incident) by itself when the scheduling fails with unexpected reason. Any other interaction with Camunda is done by the scheduled Robot Framework bot, mostly using a dedicated Robot Framework listener library.\n\nThis initial preview provides support for local parallel task execution, but the concept is designed to support also remote executors, like parameterized Nomad tasks, CI systems, Docker or even Robocloud API.\n\nRequirements:\n\n* Docker with Docker Compose for Camunda\n\n* Python >= 3.8 for executing Robot Framework\n\n  ```bash\n  $ python --version\n  Python 3.8.8\n  ```\n\n* NodeJS >= 12 for executing the external task client\n\n  ```\n  $ node --version\n  v12.21.0\n  ```\n\n\nTrying it out\n=============\n\nWhile `carrot-executor` itself can be installed from PyPI, trying out the concept requires setting up Camunda BPM Platform and having the example Robot Framework task suites.\n\nThe easiest way for all this is to clone or download the project repository and starting the preconfigured Camunda with Docker Compose:\n\n```bash\n$ git clone https://github.com/datakurre/carrot-executor\n$ cd carrot-executor\n$ docker-compose up\n```\n\nAfter everything is ready, there should be Camunda running at http://localhost:8080/camunda with username `demo` and password `demo`.\n\nBy default, our Camunda container has both theirs and ours demo processes deployed. Let\'s get rid of their demo processes:\n\n1. Open Camunda Tasklist: http://localhost:8080/camunda/app/tasklist/default/\n2. Choose **Start process**\n3. Choose **Reset Camunda to clear state** and\n4. Press **Start**\n\nThe started process could now be completed with the help of `carrot-executor`. For that we need to create a new Python environment with our package:\n\n```bash\n$ python -m venv my-carrot-executor\n$ source my-carrot-executor/bin/activate\n$ pip install carrot-executor\n```\n\nThe executor may now be started with parameterizing it to complete tasks from the process we started:\n\n```bash\n$ CAMUNDA_API_PATH=http://localhost:8080/engine-rest ROBOT_SUITE=$(pwd)/robot/reset.robot CAMUNDA_TOPIC="Delete all tasklist filters,Delete all deployments" carrot-executor\npolling\n✓ subscribed to topic Delete all tasklist filters\n✓ subscribed to topic Delete all deployments\npolling\n✓ polled 2 tasks\npolling\n✓ polled 0 tasks\n```\n\nBy default, the executor executes the task name matching with the subscribed topic name. This can be overridden with environment variable `ROBOT_TASK`. Setting the variable empty, should execute full suite.\n',
    'author': 'Asko Soukka',
    'author_email': 'asko.soukka@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datakurre/carrot-executor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
