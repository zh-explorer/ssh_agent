import json
import jsonschema
from .context import context
from .conf_schema import schema as schema_data

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
        context[i] = main_conf[i]

    for server in conf["servers"]:
        server_validator.validate(server)
        if "pkey" not in server and "password" not in server:
            if "main_pkey" in main_conf:
                server['pkey'] = main_conf["main_key"]
            if "main_password" in main_conf:
                server["password"] = main_conf["main_password"]
            raise jsonschema.ValidationError("not password or pkey")
        if 'timeout' not in server:
            server['timeout'] = main_conf['timeout']

    context['servers'] = conf["servers"]


def load_conf_file(filename):
    make_validator()
    conf = load_json(filename)
    load_conf(conf)
