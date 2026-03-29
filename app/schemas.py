from marshmallow import Schema, fields, validate, pre_load, RAISE

class BaseSchema(Schema):
    @pre_load
    def sanitise_strings(self, data, **kwargs):
        return {
            k: v.strip() if isinstance(v, str) else v
            for k, v in data.items()
        }


class RegisterSchema(BaseSchema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=80),
            validate.Regexp(
                r'^[a-zA-Z0-9_-]+$',
                error='username may only contain letters, numbers, hyphens and underscores'
            )
        ]
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=72)
    )


class LoginSchema(BaseSchema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=1, max=72))


class CoinCreateSchema(BaseSchema):
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=35),
            validate.Regexp(
                r'^[a-zA-Z0-9 _-]+$',
                error='name may only contain letters, numbers, spaces, hyphens and underscores'
            )
        ]
    )
    description = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=255),
            validate.Regexp(
                r'^[a-zA-Z0-9 .,!?_-]+$',
                error='description contains invalid characters'
            )
        ]
    )


class CoinPatchSchema(BaseSchema):
    name = fields.Str(
        validate=[
            validate.Length(min=1, max=35),
            validate.Regexp(
                r'^[a-zA-Z0-9 _-]+$',
                error='name may only contain letters, numbers, spaces, hyphens and underscores'
            )
        ]
    )
    description = fields.Str(
        validate=[
            validate.Length(min=1, max=255),
            validate.Regexp(
                r'^[a-zA-Z0-9 .,!?_-]+$',
                error='description contains invalid characters'
            )
        ]
    )
    complete = fields.Bool()


class CoinDutySchema(BaseSchema):
    duty_id = fields.Str(required=True, validate=validate.Length(min=1))



class DutyCreateSchema(BaseSchema):
    name = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=3),
            validate.Regexp(
                r'^[A-Z0-9]+$',
                error='name may only contain uppercase letters and numbers'
            )
        ]
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=255)
    )


class DutyPatchSchema(BaseSchema):
    name = fields.Str(
        validate=[
            validate.Length(min=1, max=3),
            validate.Regexp(
                r'^[A-Z0-9]+$',
                error='name may only contain uppercase letters and numbers'
            )
        ]
    )
    description = fields.Str(
        validate=validate.Length(min=1, max=255)
    )