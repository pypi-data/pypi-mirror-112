from datetime import timedelta
from typing import Callable, Any, Set, NamedTuple, List, TYPE_CHECKING, Generic, TypeVar, Type
from uuid import UUID

from pydantic import ValidationError

from unipipeline.modules.uni_message_codec import UniMessageCodec
from unipipeline.modules.uni_definition import UniDynamicDefinition
from unipipeline.modules.uni_echo import UniEcho
from unipipeline.modules.uni_broker_definition import UniBrokerDefinition
from unipipeline.modules.uni_message_meta import UniMessageMeta

if TYPE_CHECKING:
    from unipipeline.modules.uni_mediator import UniMediator


class UniBrokerMessageManager:
    def reject(self) -> None:
        raise NotImplementedError(f'method reject must be specified for class "{type(self).__name__}"')

    def ack(self) -> None:
        raise NotImplementedError(f'method acknowledge must be specified for class "{type(self).__name__}"')


class UniBrokerConsumer(NamedTuple):
    topic: str
    id: str
    group_id: str
    message_handler: Callable[[UniMessageMeta, UniBrokerMessageManager], None]


TConf = TypeVar('TConf')


class UniBroker(Generic[TConf]):
    config_type: Type[TConf] = UniDynamicDefinition  # type: ignore

    def __init__(self, mediator: 'UniMediator', definition: UniBrokerDefinition) -> None:
        self._uni_definition = definition
        self._uni_mediator = mediator
        self._uni_echo = self._uni_mediator.echo.mk_child(f'broker[{self._uni_definition.name}]')

        try:
            self._uni_conf = self._uni_definition.configure_dynamic(self.config_type)  # type: ignore
        except ValidationError as e:
            self._uni_echo.exit_with_error(str(e))

    @property
    def config(self) -> TConf:
        return self._uni_conf

    def codec_serialize(self, meta: UniMessageMeta) -> bytes:
        meta_dumps = self.definition.codec.dumps(meta.dict())
        meta_compressed = self.definition.codec.compress(meta_dumps)
        return meta_compressed

    def codec_parse(self, content: bytes, codec: UniMessageCodec = None) -> UniMessageMeta:
        if codec is None:
            codec = self.definition.codec
        body_uncompressed = codec.decompress(content)
        body_json = codec.loads(body_uncompressed)
        return UniMessageMeta(**body_json)

    def connect(self) -> None:
        raise NotImplementedError(f'method connect must be implemented for {type(self).__name__}')

    def close(self) -> None:
        raise NotImplementedError(f'method close must be implemented for {type(self).__name__}')

    def add_consumer(self, consumer: UniBrokerConsumer) -> None:
        raise NotImplementedError(f'method consume must be implemented for {type(self).__name__}')

    def stop_consuming(self) -> None:
        raise NotImplementedError(f'method stop_consuming must be implemented for {type(self).__name__}')

    def start_consuming(self) -> None:
        raise NotImplementedError(f'method start_consuming must be implemented for {type(self).__name__}')

    def publish(self, topic: str, meta_list: List[UniMessageMeta]) -> None:
        raise NotImplementedError(f'method publish must be implemented for {type(self).__name__}')

    def get_topic_approximate_messages_count(self, topic: str) -> int:
        raise NotImplementedError(f'method get_topic_size must be implemented for {type(self).__name__}')

    def initialize(self, topics: Set[str], answer_topics: Set[str]) -> None:
        raise NotImplementedError(f'method initialize must be implemented for {type(self).__name__}')

    def get_answer(self, answer_topic: str, answer_id: UUID, max_delay_s: int) -> UniMessageMeta:
        raise NotImplementedError(f'method initialize must be implemented for {type(self).__name__}')

    def publish_answer(self, answer_topic: str, answer_id: UUID, meta: UniMessageMeta) -> None:
        raise NotImplementedError(f'method publish_answer must be implemented for {type(self).__name__}')

    @property
    def definition(self) -> UniBrokerDefinition:
        return self._uni_definition

    @property
    def echo(self) -> UniEcho:
        return self._uni_echo
