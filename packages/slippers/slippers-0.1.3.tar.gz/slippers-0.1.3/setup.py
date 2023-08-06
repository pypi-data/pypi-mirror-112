# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slippers', 'slippers.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2,<4.0', 'PyYAML>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'slippers',
    'version': '0.1.3',
    'description': 'Slippers is a lightweight library for Django that makes your HTML components available as template tags.',
    'long_description': '# Slippers\n\nSlippers is a lightweight library for Django that makes your HTML components available as template tags.\n\n```django\n{% card variant="small" %}\n  <h1>Slippers is cool</h1>\n\n  {% button %}Super cool{% endbutton %}\n  {% button variant="secondary" %}Lit af{% endbutton %}\n{% endcard %}\n```\n\n## Why?\n\nI want to be able to make reusable components, but the syntax for `{% include %}` is too verbose. Plus it doesn\'t allow me to specify child elements.\n\n## Show me how it works\n\nFirst create your template. Wherever you would normally put it is fine.\n\n```django\n{# myapp/templates/myapp/card.html #}\n<div class="card">\n  <h1 class="card__header">{{ heading }}</h1>\n  <div class="card__body">\n    {# Child elements are rendered by `{{ children }}` #}\n    {{ children }}\n  </div>\n</div>\n```\n\nNext, create a `components.yaml` file. By default, Slippers looks for this file in the root template folder.\n\n```yaml\n# myapp/templates/components.yaml\n# Components that have child elements\nblock_components:\n  card: "myapp/card.html"\n \n# Components that don\'t have child elements\ninline_components: \n  avatar: "myapp/avatar.html"\n```\n\nYou can now use the components like so:\n\n```django\n{% load slippers %}\n\n{% card heading="Slippers is awesome" %}\n  <span>Hello {{ request.user.full_name }}!</span>\n{% endcard %}\n```\n\nAnd the output:\n\n```html\n<div class="card">\n  <h1 class="card__header">Slippers is awesome</h1>\n  <div class="card__body">\n    <span>Hello Ryland Grace!</span>\n  </div>\n</div>\n```\n\n## Installation\n\n```\npip install slippers\n```\n\nAdd it to your `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = [\n    ...\n    \'slippers\',\n    ...\n]\n```\n\n## Documentation\n\n### The `components.yaml` file\n\nThis file should be placed at the root template directory. E.g. `myapp/templates/components.yaml`.\n\nThe structure of the file is as follows:\n\n```yaml\n# Components that have child elements are called "block" components\nblock_components:\n  # The key determines the name of the template tag. So `card` would generate\n  # `{% card %}{% endcard %}`\n  # The value is the path to the template file as it would be if used with {% include %}\n  card: "myapp/card.html"\n \n# Components that don\'t have child elements are called "inline" components\ninline_components: \n  avatar: "myapp/avatar.html"\n```\n\nThis file also doubles as an index of available components which is handy.\n\n### Context\n\nUnlike `{% include %}`, using the component template tag **will not** pass the\ncurrent context to the child component. This is a design decision. If you need\nsomething from the parent context, you have to explicitly pass it in via keyword\narguments, or use `{% include %}` instead.\n\n```django\n{% with not_passed_in="Lorem ipsum" %}\n  {% button is_passed_in="Dolor amet" %}Hello{% endbutton %}\n{% endwith %}\n```\n\n## License\n\nMIT\n',
    'author': 'Mitchel Cabuloy',
    'author_email': 'mixxorz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mixxorz/slippers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
