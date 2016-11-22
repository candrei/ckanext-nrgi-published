from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h

from webhelpers.html import literal


def extended_build_nav(*args):
    # we go through the args, add links for raw links,
    # and then pass the rest to core build_nav_main
    output = ''
    for item in args:
        menu_item, title = item[:2]

        if len(item) == 3 and not toolkit.check_access(item[2]):
            continue

        if menu_item.startswith('http') or menu_item.startswith('/'):
            # it's a link
            output += literal(
                '<li><a href="%s">%s</a></li>' % (menu_item, title)
            )
        else:
            # give it to the core helper for this
            output += h._make_menu_item(menu_item, title)
    return output


class NrgiPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'nrgi')

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'extended_build_nav': extended_build_nav,
        }

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        if (package_type == 'dataset'):
            facets_dict = OrderedDict([
                ('country', toolkit._('Country')),
                ('year', toolkit._('Year')),
                ('assessment_type', toolkit._('Assessment Type')),
                # ('category', plugins.toolkit._('Categories')),
                ('tags', toolkit._('Tags')),
                ('res_format', toolkit._('Formats')),
                ('license_id', toolkit._('Licenses')),
                ('openness_score', toolkit._('Openness'))
            ])
        return facets_dict

    # IRoutes

    def after_map(self, map):
        map.connect('resource_search', '/resource_search',
                    controller='ckanext.nrgi.controller:NrgiController',
                    action='search')
        return map
