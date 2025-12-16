# --- 1. New Helper Function ---
def _format_decimal_as_int_or_float(value):
    """Converts a float/Decimal to int if it has no decimal part."""
    if value is None:
        return None
    try:
        float_val = float(value)
        if float_val == int(float_val):
            return int(float_val)
        return float_val
    except (ValueError, TypeError):
        return value  # Return original value if conversion fails


# --- 2. New Mixin for to_representation logic ---
class FloatToIntRepresentationMixin:
    """
    Mixin to convert specified float/decimal fields to int in representation
    if they are whole numbers.

    Serializers using this mixin should define:
    float_to_int_fields = ["field1", "field2"]
    """

    float_to_int_fields = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field_name in self.float_to_int_fields:
            if field_name in data:
                value = data.get(field_name)
                data[field_name] = _format_decimal_as_int_or_float(value)
        return data
