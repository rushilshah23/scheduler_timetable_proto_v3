from marshmallow import Schema, fields

# Base schema for Day
class DayBaseSchema(Schema):
    id = fields.String(required=True)
    day_name = fields.String(required=True)

class WorkingDayBaseSchema(Schema):
    id = fields.String(required=True)
    day_id = fields.String(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    slot_duration = fields.Integer(required=True)
    division_id = fields.String(required=True)

class SlotBaseSchema(Schema):
    id = fields.String(required=True)
    start_time = fields.Time(required=True)
    end_time = fields.Time(required=True)
    working_day_id = fields.String(required=True)
    daily_slot_number = fields.Integer(required=True)
    weekly_slot_number = fields.Integer(required=True)

# ORM Mode Equivalents
class DaySchema(DayBaseSchema):
    class Meta:
        # ORM-friendly metadata can be added here, if necessary
        pass

class WorkingDaySchema(WorkingDayBaseSchema):
    class Meta:
        pass

class SlotSchema(SlotBaseSchema):
    class Meta:
        pass
