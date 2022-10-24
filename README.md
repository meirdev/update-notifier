# Update Notifier

Notify for updates. Inspired by https://github.com/yeoman/update-notifier.

## Example

```python
from update_notifier import update_notifier
from update_notifier.latest_version import PyPi
from update_notifier.notification import Poetry

__title__ = "requests"
__version__ = "0.1.0"

update_notifier_mytest = update_notifier(
    name=__title__,
    current_version=__version__,
    latest_version=PyPi("requests"),
)

update_notifier_mytest.notify(Poetry())
```

## Image

![image](./assets/image.svg)
