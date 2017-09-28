#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from urllib.parse import urlencode

import sockgen


app = Flask(__name__)


def form_input(request):
    # result dict with each parameter as a tuple of (value, error)
    # units is a choice field, so no error option
    if request.args == {}:
        # no url params passed - default to yes
        include_gusset = 'yes'
    else:
        # url params passed - include_gusset is yes if checked,
        # else not included
        include_gusset = request.args.get('include_gusset', 'no')
    result = {
        'units': request.args.get('units', 'inches'),
        'stitches': request.args.get('stitches', 36),
        'rows': request.args.get('rows', 40),
        'circum': request.args.get('circum', 8.5),
        'instep': request.args.get('instep', 9.5),
        'foot_length': request.args.get('foot_length', 9.25),
        'ease': request.args.get('ease', -8),
        'divisible_by': request.args.get('divisible_by', 1),
        'include_gusset': include_gusset,
    }
    errors = []

    for param in ['stitches', 'rows', 'circum', 'instep', 'foot_length', 'ease']:
        try:
            result.update({param: float(result[param])})
        except ValueError:
            errors.append(param)

    try:
        result.update({'divisible_by': int(result['divisible_by'])})
    except ValueError:
        errors.append('divisible_by')
    return result, errors


@app.route('/')
def form():
    input_fields, error_list = form_input(request)
    return render_template(
        'form.html', data=input_fields, error_list=error_list
    )


@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/foot-measurement-charts')
def foot_measurement_charts():
    return render_template('charts.html')

@app.route('/pattern')
def pattern():
    data, error_list = form_input(request)

    if error_list:
        url_values = {
            'units': data['units'],
            'stitches': data['stitches'],
            'rows': data['rows'],
            'circum': data['circum'],
            'instep': data['instep'],
            'foot_length': data['foot_length']['value'],
            'ease': data['ease']['value'],
            'divisible_by': data['divisible_by'],
            'include_gusset': data['include_gusset']
        }

        url = '/?' + urlencode(url_values)

        return redirect(url)
    if data['include_gusset'] == 'no':
        data.update(instep=data['circum'])

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


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
