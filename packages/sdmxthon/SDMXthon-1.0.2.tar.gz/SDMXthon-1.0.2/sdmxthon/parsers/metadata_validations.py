import logging

logger = logging.getLogger('logger')


def _set_on_component(comp, obj, missing_rep):
    control_errors = False
    if comp.concept_identity is not None:
        if (obj.structures.concepts is not None and
                comp.concept_identity['CS'] in obj.structures.concepts.keys()):
            if (comp.concept_identity['CON'] in
                    obj.structures.concepts[
                        comp.concept_identity['CS']].items.keys()):
                comp.concept_identity = obj.structures.concepts[
                    comp.concept_identity['CS']].items[
                    comp.concept_identity['CON']]
            else:
                if comp.concept_identity['CON'] not in missing_rep['CON']:
                    missing_rep['CON'].append(comp.concept_identity['CON'])
                control_errors = True

        else:
            if comp.concept_identity['CS'] not in missing_rep['CS']:
                missing_rep['CS'].append(comp.concept_identity['CS'])
            control_errors = True

    if comp.local_representation is not None:
        if comp.local_representation.codelist is not None:
            if (obj.structures.codelists is not None and
                    comp.local_representation.codelist in
                    obj.structures.codelists.keys()):
                comp.local_representation.codelist = obj.structures.codelists[
                    comp.local_representation.codelist]
            else:
                if comp.local_representation.codelist not in missing_rep['CL']:
                    missing_rep['CL'].append(
                        comp.local_representation.codelist
                    )
                control_errors = True

        elif comp.local_representation.concept_scheme is not None:
            if (obj.structures.concepts is not None and
                    comp.local_representation.concept_scheme in
                    obj.structures.concepts.keys()):
                comp.local_representation.concept_scheme = \
                    obj.structures.concepts[
                        comp.local_representation.concept_scheme]
            else:
                if comp.concept_identity['CS'] not in missing_rep['CS']:
                    missing_rep['CS'].append(comp.concept_identity['CS'])
                control_errors = True

    return control_errors


def _check_relationship(att, dsd, obj):
    if (isinstance(att.related_to['id'], list) and
            att.related_to['type'] == 'Dimension'):
        relations = att.related_to['id'].copy()
        att.related_to = {}
        for i in relations:
            if i in dsd.dimension_codes:
                att.related_to[i] = dsd.dimension_descriptor.components[i]
            else:
                obj.structures.add_error(
                    {'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                     'ObjectID': f'{dsd.unique_id}-'
                                 f'{dsd.attribute_descriptor.id}',
                     'ObjectType': 'Attribute',
                     'Message': f'Missing Dimension {i} related to Attribute '
                                f'{att.id}'})
    else:
        if att.related_to['type'] == 'Dimension':
            if att.related_to['id'] in dsd.dimension_codes:
                att.related_to = dsd.dimension_descriptor.components[
                    att.related_to['id']]
            else:
                obj.structures.add_error(
                    {'Code': 'MS04', 'ErrorLevel': 'CRITICAL',
                     'ObjectID': f'{dsd.unique_id}-'
                                 f'{dsd.attribute_descriptor.id}',
                     'ObjectType': 'Attribute',
                     'Message': f'Missing Dimension {att.related_to["id"]} '
                                f'related to Attribute '
                                f'{att.id}'})
        elif att.related_to['type'] == 'PrimaryMeasure':
            if att.related_to['id'] in dsd.measure_code:
                att.related_to = dsd.measure_descriptor.components[
                    att.related_to['id']]
            else:
                obj.structures.add_error(
                    {'Code': 'MS05', 'ErrorLevel': 'CRITICAL',
                     'ObjectID': f'{dsd.unique_id}-'
                                 f'{dsd.attribute_descriptor.id}',
                     'ObjectType': 'Attribute',
                     'Message': 'Missing Primary Measure '
                                f'{att.related_to["id"]} '
                                f'related to Attribute {att.id}'})


def _set_references(obj):
    """ Metadata validations stands for the next schema:

        .. list-table:: Metadata validations
            :widths: 20 80
            :header-rows: 1

            * - Code
              - Description
            * - MS01
              - Check that the metadata file contains at least one DSD
            * - MS02
              - Check that the metadata file contains related codelists
            * - MS03
              - Check if the DSD metadata file contains the concepts needed \
                for each DSD
            * - MS04
              - Check if the dimensions in Attribute Relationship are in \
                DimensionList in DSD file
            * - MS05
              - Check if the primary measure in Attribute Relationship is in
                MeasureList in DSD file
            * - MS06
              - Check if all DSDs present in the metadata file are unique
            * - MS07
              - Check if all Concept Scheme needed are present
            * - MX01
              - Check if minimum structural requirements for DSD xml are \
                satisfied
            * - MX02
              - Check if every DSD has primary measure defined
            * - MX04
              - Check if every Codelist is defined in each reference from \
                Concepts

    """

    agencies = {}
    if obj.structures.organisations is not None and len(
            obj.structures.organisations.items) > 0:
        agencies = obj.structures.organisations.items
        if obj.structures.organisations.maintainer in agencies.keys():
            obj.structures.organisations.maintainer = agencies[
                obj.structures.organisations.maintainer]

    if obj.structures.codelists is not None:
        for cl in obj.structures.codelists.values():
            if cl.maintainer in agencies.keys():
                cl.maintainer = agencies[cl.maintainer]

    if obj.structures.concepts is not None:
        for sch in obj.structures.concepts.values():
            if sch.maintainer in agencies.keys():
                sch.maintainer = agencies[sch.maintainer]
            for con in sch.items.values():
                if con.id in sch.cl_references.keys():
                    cl = sch.cl_references[con.id]
                    if obj.structures.codelists is not None and \
                            cl in obj.structures.codelists.keys():
                        sch.items[con.id].core_representation.codelist = \
                            obj.structures.codelists[cl]
                    else:
                        obj.structures.add_error(
                            {'Code': 'MX04', 'ErrorLevel': 'CRITICAL',
                             'ObjectID': f'{sch.unique_id}-{con.id}',
                             'ObjectType': 'Concept',
                             'Message': f'Codelist {cl} not found for '
                                        f'Concept {sch.unique_id}-{con.id}'})

    if obj.structures.dsds is not None:
        mr = {'CS': [], 'CL': [], 'CON': []}
        keys_errors = []
        for key, dsd in obj.structures.dsds.items():
            if dsd.maintainer in agencies.keys():
                dsd.maintainer = agencies[dsd.maintainer]
            if dsd.dimension_descriptor is not None:
                for dim in dsd.dimension_descriptor.components.values():
                    control_errors = _set_on_component(comp=dim, obj=obj,
                                                       missing_rep=mr)
                    if control_errors and key not in keys_errors:
                        keys_errors.append(key)

            else:
                if key not in keys_errors:
                    keys_errors.append(key)
                obj.structures.add_error(
                    {'Code': 'MX01', 'ErrorLevel': 'CRITICAL',
                     'ObjectID': f'{dsd.unique_id}', 'ObjectType': 'DSD',
                     'Message': f'DSD {dsd.unique_id} does not have '
                                f'a DimensionList'})

            if dsd.attribute_descriptor is not None:
                for att in dsd.attribute_descriptor.components.values():
                    control_errors = _set_on_component(comp=att, obj=obj,
                                                       missing_rep=mr
                                                       )
                    if control_errors and key not in keys_errors:
                        keys_errors.append(key)
                    if (att.related_to is not None and
                            att.related_to != 'NoSpecifiedRelationship'):
                        _check_relationship(att, dsd, obj)

            if dsd.measure_descriptor is not None:
                if len(dsd.measure_descriptor.components) == 1:
                    for meas in dsd.measure_descriptor.components.values():
                        control_errors = _set_on_component(
                            comp=meas, obj=obj, missing_rep=mr)

                        if control_errors and key not in keys_errors:
                            keys_errors.append(key)

                else:
                    if key not in keys_errors:
                        keys_errors.append(key)
                    obj.structures.add_error(
                        {'Code': 'MX02', 'ErrorLevel': 'CRITICAL',
                         'ObjectID': f'{dsd.unique_id}',
                         'ObjectType': 'DSD',
                         'Message': f'DSD {dsd.unique_id} does not have'
                                    f' a Primary Measure'})

            if dsd.group_dimension_descriptor is not None:
                for gr in dsd.group_dimension_descriptor.components.keys():
                    if gr in dsd.dimension_descriptor.components.keys():
                        dsd.group_dimension_descriptor.components[gr] = \
                            dsd.dimension_descriptor.components[gr]
                    else:
                        # TODO Error Dimension not found
                        pass

        _grouping_errors(mr, obj, keys_errors)
    else:
        obj.structures.add_error(
            {'Code': 'MS01', 'ErrorLevel': 'CRITICAL', 'ObjectID': None,
             'ObjectType': 'DSD',
             'Message': 'Not found any DSD in this file'})

    if (obj.structures.dsds is not None and
            obj.structures.dataflows is not None):
        for key, flow in obj.structures.dataflows.items():
            if flow.structure in obj.structures.dsds.keys():
                flow.structure = obj.structures.dsds[flow.structure]

    if obj.structures.constraints is not None:
        for const in obj.structures.constraints.values():
            if (const.type_attach == 'DataStructure' and
                    obj.structures.dsds is not None and
                    const.ref_attach in obj.structures.dsds.keys()):
                obj.structures.dsds[const.ref_attach].add_constraint(const)

            elif (const.type_attach == 'Dataflow' and
                  obj.structures.dataflows is not None and
                  const.ref_attach in obj.structures.dataflows.keys()):
                obj.structures.dataflows[const.ref_attach].add_constraint(
                    const)


def _grouping_errors(missing_rep, obj, keys_errors):
    for k in keys_errors:
        del obj.structures.dsds[k]

    if len(missing_rep['CL']) > 0:
        for e in missing_rep['CL']:
            obj.structures.add_error({'Code': 'MS02', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}',
                                      'ObjectType': 'Codelist',
                                      'Message': f'Missing Codelist {e}'})

    if len(missing_rep['CS']) > 0:
        for e in missing_rep['CS']:
            obj.structures.add_error({'Code': 'MS07', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}',
                                      'ObjectType': 'Concept',
                                      'Message': f'Missing Concept Scheme {e}'}
                                     )

    if len(missing_rep['CON']) > 0:
        for e in missing_rep['CON']:
            obj.structures.add_error({'Code': 'MS03', 'ErrorLevel': 'CRITICAL',
                                      'ObjectID': f'{e}',
                                      'ObjectType': 'Concept',
                                      'Message': f'Missing Concept {e}'})
