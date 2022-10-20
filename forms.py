from wtforms import Form, BooleanField, StringField, FloatField,IntegerField,RadioField, validators

class PatternGeneratorForm(Form):
    units = RadioField('Units', choices=(("inches", "inches") , ("cms", "cms")), default="inches")
    stitches = FloatField('Gauge: rows per 4in/10cm', default=36.0)
    rows = FloatField('Gauge: Stitches per 4in/10cm', default=40.0)
    circum =  FloatField('Foot circumference', default=8.5)
    foot_length =  FloatField('Foot length', default=9.5)
    include_gusset =  BooleanField('Include gusset increases?', default=True)
    instep =  FloatField('Instep circumference', default=9.5)
    ease =  IntegerField('Ease (%)', default=-8)
    divisible_by =  IntegerField('Number of stitches in pattern repeat', default=1)
