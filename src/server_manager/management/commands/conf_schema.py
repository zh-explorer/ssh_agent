schema = {
    "servers": {
        "definitions": {
            "host_list": {
                "anyOf": [
                    {
                        "type": "string",
                        "format": "string"
                    },
                    {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "host_name": {
                                    "type": "string"
                                },
                                "host": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                ]
            },
            "port_list": {
                "anyOf": [
                    {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 65535,
                    },
                    {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "server_name": {
                                    "type": "string"
                                },
                                "port": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 65535,
                                }
                            }
                        }
                    }
                ]
            }
        },
        "title": "ssh server schema",
        "description": "check ssh server config",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "name": {
                "type": "string"
            },
            "host": {
                "$ref": "#/definitions/host_list"
            },
            "pkey": {
                "type": "string"
            },
            "port": {
                "type": "integer",
                "minimum": 0,
                "maximum": 65535,
                "default": 22
            },
            "user": {
                "type": "string",
                "default": "root"
            },
            "password": {
                "type": "string"
            },
            'challenge_port': {
                "$ref": "#/definitions/port_list"
            },
            "tags": {
                "type": "array",
                "item": {
                    "minItem": 1,
                    "type": "string"
                }
            }
        },
        "required": [
            "name",
            "host"
        ]
    },
    "config": {
        "title": "ssh main schema",
        "description": "ssh main config",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "timeout": {
                "type": "integer",
                "default": 30
            },
            "main_pkey": {
                "type": "string",
            },
            "main_password": {
                "type": "string",
            }
        }

    }
}
