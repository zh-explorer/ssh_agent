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
                        "items": {
                            "type": "object",
                            "properties": {
                                "host_name": {
                                    "type": "string"
                                },
                                "ip": {
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
                        "items": {
                            "type": "object",
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
        "properties": {
            "timeout": {
                "type": "integer",
                "default": 30
            },
            "main_key": {
                "type": "string",
            }
        }
    }
}
