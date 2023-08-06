# Chamallow

...

## Install

...

### Local Usage Only

...

```bash
(venv)$ pip install chamallow
```

### Distributed Usage

...

```bash
(venv)$ pip install chamallow[zmq]
```

## Func Dispatching

...

### From YAML

...

```python
# funcs.py
def ping(a, k=None):
    return f"{a} and {k}"


def pong(a):
    print(a)
```

...

```yaml
# demo.yml
ping:
  name: "funcs.ping"
  args:
    - "foo"
  kwargs:
    k: "bar"
  tags:
    - "foo"
pong:
  name: "funcs.pong"
  args:
    - _from: "ping"
```

...

```bash
(venv)$ CHAMALLOW_TAGS=foo chamallow demo.yml
foo and bar
```

### With Decorators

...

```python
# demo.py
from chamallow import engine, flow

@flow(tags=("foo",))
def ping(a, k=None):
    return f"{a} and {k}"


@flow()
def pong(a):
    print(a)
    return True


if __name__ == "__main__":
    engine.start()
    assert pong(ping("foo", k="bar")).result() is True
    engine.stop()
```

...

```bash
(venv)$ CHAMALLOW_TAGS=foo python demo.py
foo and bar
```

## Hacking

...

### CLI

...

```bash
(venv)$ chamallow
```

### Docker

...

```bash
$ docker-compose up -d
$ docker-compose exec chamallow bash -c "chamallow examples/simple.yml"
$ docker-compose exec chamallow-client bash -c "cat simple.csv simple.json"
foo;bar
xxx;YYY
{
  "foo": "xxx",
  "bar": "YYY"
}
```

## Settings

- ADDRESS
- CACHE_TTL
- CONNECT_PORT
- DEBUG
- LOCAL
- LOG_FORMAT
- POLLING_INTERVAL
- NUMBER_OF_CLIENTS
- NUMBER_OF_REMOTE_CLIENTS
- TAGS

## Contributing

...

### Linting

...

```bash
(venv)$ pip install chamallow[lint]
(venv)$ pre-commit run --all-files
```

### Testing

...

```bash
(venv)$ pip install chamallow[test]
(venv)$ CHAMALLOW_LOCAL=True pytest tests/
```

## License

MIT
