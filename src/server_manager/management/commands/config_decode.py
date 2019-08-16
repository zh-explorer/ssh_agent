import json
import jsonschema
from .conf_schema import schema as schema_data
from server_manager.models import Host, Server, Tag, ChallengePort, Config

from django.db.models import ObjectDoesNotExist

server_validator = None
config_validator = None


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
                validator, properties, instance, schema,
        ):
            yield error

    return jsonschema.validators.extend(
        validator_class, {"properties": set_defaults},
    )


def load_json(file_name):
    with open(file_name, 'r') as fp:
        data = fp.read()
    return json.loads(data)


def make_validator():
    global server_validator, config_validator
    server_schema, config_schema = schema_data["servers"], schema_data["config"]
    default_validating = extend_with_default(jsonschema.Draft4Validator)
    server_validator = default_validating(server_schema, format_checker=jsonschema.FormatChecker())
    config_validator = default_validating(config_schema, format_checker=jsonschema.FormatChecker())


def load_conf(conf):
    main_conf = conf["config"]
    config_validator.validate(main_conf)

    for i in main_conf:
        Config.objects.update_or_create(key=i, defaults={"value": main_conf[i]})

    for server in conf["servers"]:
        server_validator.validate(server)
        host = server["host"]
        del server["host"]

        if "challenge_port" in server:
            challenge_port = server["challenge_port"]
            del server["challenge_port"]
        else:
            challenge_port = None

        if "tags" in server:
            tags = server["tags"]
            del server['tags']
        else:
            tags = None

        s = Server(**server)
        s.save()
        if isinstance(host, str):
            Host(host=host, server=s).save()
        else:
            for i in host:
                i["server"] = s
                Host(**i).save()

        if challenge_port is not None:
            if isinstance(challenge_port, int):
                ChallengePort(port=challenge_port, server=s).save()
            else:
                for i in challenge_port:
                    i['server'] = s
                    ChallengePort(**i).save()

        if tags is not None:
            for tag in tags:
                t, _ = Tag.objects.get_or_create(name=tag)
                s.tag.add(t)
        s.save()


def load_conf_file(filename):
    make_validator()
    conf = load_json(filename)
    load_conf(conf)
