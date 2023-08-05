from enum import IntEnum
from typing import Dict, Any, Optional

from robotnikmq import Topic, Message, RobotnikConfig
from typeguard import typechecked


@typechecked
class Priority(IntEnum):
    INFO = 0
    ACTIVITY = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


@typechecked
def broadcast(exchange: str,
              route: str,
              priority: Priority,
              contents: Dict[str, Any],
              ttl: Optional[int] = None,
              description: Optional[str] = None,
              alert_key: Optional[str] = None,
              config: Optional[RobotnikConfig] = None):
    _contents: Dict[str, Any] = {'priority': priority.value}
    if priority.value >= 2:
        assert description is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have a description'
        assert ttl is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have a ttl (to clear an alert, set the ttl to 0)'
        assert alert_key is not None, 'Alerts (e.g. WARNING, ERROR, CRITICAL) must have an alert_key'
    if ttl is not None:
        _contents['ttl'] = ttl
    if description is not None:
        _contents['description'] = description
    if alert_key is not None:
        _contents['alert_key'] = alert_key
    _contents.update(contents)
    route += f'.{priority.name.lower()}'
    Topic(exchange=exchange, config=config).broadcast(Message(contents=_contents),
                                                      routing_key=route)


@typechecked
def broadcast_info(exchange: str, route: str, contents: Dict[str, Any],
                   config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, priority=Priority.INFO, contents=contents, config=config)


@typechecked
def broadcast_activity(exchange: str, route: str, contents: Dict[str, Any],
                       config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, priority=Priority.ACTIVITY, contents=contents, config=config)


@typechecked
def broadcast_alert(exchange: str,
                    route: str,
                    description: str,
                    alert_key: str,
                    contents: Dict[str, Any],
                    ttl: int = 30,
                    priority: Priority = Priority.WARNING,
                    config: Optional[RobotnikConfig] = None):
    broadcast(exchange, route, ttl=ttl, priority=priority, contents=contents,
              config=config, description=description, alert_key=alert_key)


@typechecked
def broadcast_warning(exchange: str, route: str, desc: str, alert_key: str,
                      contents: Dict[str, Any], ttl: int = 30,
                      config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.WARNING, config=config)


@typechecked
def broadcast_error(exchange: str, route: str, desc: str, alert_key: str,
                    contents: Dict[str, Any], ttl: int = 30,
                    config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.ERROR, config=config)


@typechecked
def broadcast_critical(exchange: str, route: str, desc: str, alert_key: str,
                       contents: Dict[str, Any], ttl: int = 30,
                       config: Optional[RobotnikConfig] = None):
    broadcast_alert(exchange, route, description=desc, alert_key=alert_key, contents=contents,
                    ttl=ttl, priority=Priority.CRITICAL, config=config)
