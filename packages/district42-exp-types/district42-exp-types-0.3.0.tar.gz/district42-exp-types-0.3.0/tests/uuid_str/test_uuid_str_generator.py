from uuid import UUID, uuid4

from baby_steps import given, then, when
from blahblah import fake

from district42_exp_types.uuid_str import schema_uuid_str


def test_uuid_str_generation():
    with given:
        sch = schema_uuid_str

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, str)
        assert str(UUID(res)) == res


def test_uuid_str_value_generation():
    with given:
        val = str(uuid4())
        sch = schema_uuid_str(val)

    with when:
        res = fake(sch)

    with then:
        assert res == val
