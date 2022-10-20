#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

import sockgen
from forms import PatternGeneratorForm

app = Flask(__name__)


@app.route('/')
def home():
    form = PatternGeneratorForm()
    return render_template(
        'home.html', form=form
    )


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    if request.method == 'POST' and "back" in request.form:
        form = PatternGeneratorForm()

        bool_map = {
            "True": True,
            "False": False,
        }
        for field, value in request.form.items():
            if field != "back":
                cleaned_value = value.rstrip("/")
                cleaned_value = bool_map.get(cleaned_value, cleaned_value)
                form_field = getattr(form, field)
                setattr(form_field, "default", cleaned_value)
        form.process()
    else:
        form = PatternGeneratorForm(request.form)
        if request.method == 'POST' and form.validate():
            data = {
                'units': form.units.data,
                'stitches': form.stitches.data,
                'rows': form.rows.data,
                'circum': form.circum.data,
                'instep': form.instep.data if form.include_gusset.data else form.circum.data,
                'foot_length': form.foot_length.data,
                'ease': form.ease.data,
                'divisible_by': form.divisible_by.data,
                'include_gusset': form.include_gusset.data
            }

            sock_info = sockgen.Pattern_info(data)
            pattern_data = sockgen.pattern(
                sock_info, data['circum'], data['foot_length'],
                data['instep'], data['divisible_by']
            )

            data.update({
                'sock_info': sock_info,
                'cast_on': pattern_data['cast_on'],
                'heel_end': pattern_data['heel_end'],
                'toe_end': pattern_data['toe_end'],
                'heel_length': pattern_data['heel_length'],
                'gusset_sts': pattern_data['gusset_sts'],
                'heel_sts': pattern_data['heel_sts'],
                'foot_length_before_gusset': pattern_data['foot_length_before_gusset']
            })

            return render_template('pattern.html', data=data)

    return render_template(
        'generator.html', form=form
    )


@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/foot-measurement-charts')
def foot_measurement_charts():
    return render_template('charts.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
