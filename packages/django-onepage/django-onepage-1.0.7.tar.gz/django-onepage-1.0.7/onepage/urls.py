from .views import *
from django.urls import path, re_path
from .validator import BasicValidator


def add_pattern(model, form, form_update=False, validator=False, scripts={}):
    meta = model._meta
    app_label = meta.app_label
    model_name = meta.model_name

    gv.model_map[model_name] = model
    gv.validator_map[model_name] = validator or BasicValidator
    gv.scripts_map[model_name] = scripts

    gv.ajax_form_map[app_label + '-' + 'add' + '-' + model_name] = form
    gv.ajax_form_map[app_label + '-' + 'change' + '-' + model_name] = form_update if form_update else form

    data_keys = ",".join(f.name for f in meta.get_fields())
    data_keys = 'id,' + data_keys.split('id,')[1]
    model_id = app_label + '-' + 'view' + '-' + model_name

    if gv.menu_map.get(app_label, 0):
        gv.menu_map[app_label]['submenu'].append({
            'id': model_id,
            'data_r_kwargs': '',
            'data_keys': data_keys,
            'title': meta.verbose_name.capitalize()
        })

    else:
        gv.menu_map[app_label] = {
            'id': app_label + 'AppMenuItem',
            'title': app_label.capitalize(),
            'submenu': [
                {
                    'id': model_id,
                    'data_r_kwargs': '',
                    'data_keys': data_keys,
                    'title': meta.verbose_name.capitalize()
                }
            ]
        }

    gv.data_map_for_list_view[model_id] = {
        'r_kwargs': '',
        'data-keys': data_keys,
        'data-post-url': '/ajax/two-act-handler/'
    }


patterns = [
    path('ajax/four-act-handler/', ajax_four_act_handler, name='ajax-four-act-handler'),
    path('ajax/two-act-handler/', ajax_two_act_handler, name='ajax-two-act-handler'),
    path('', onepage_home, name='onepage-home'),
    re_path(r'^(?P<props>[\w-]+)/', ajax_four_act_handler, name="ajax-one-page-view")
]
