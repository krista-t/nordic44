from nordic44.classes import ACLineSegment, Substation


PREFIXES = {
   "cim":"http://iec.ch/TC57/2013/CIM-schema-cim16#" ,
    "icim":"http://iec.ch/TC57/2013/CIM-schema-cim16-info#" ,
    "entsoe":"http://entsoe.eu/CIM/SchemaExtension/3/1#",
    "entsoe2":"http://entsoe.eu/CIM/SchemaExtension/3/2#" ,
    "md":"http://iec.ch/TC57/61970-552/ModelDescription/1#" ,
    "pti":"http://www.pti-us.com/PTI_CIM-schema-cim16#" ,
    "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#"
}


def count_instances(xml_root_elements: list, object_type: str, namespace: str = "http://iec.ch/TC57/2013/CIM-schema-cim16#" ) -> int:
    """Count instances of given object type in list of xml root elements

    Parameters
    ----------
    xml_root_elements : list
        List of xml root elements
    object_type : str
        Name of object type
    namespace : str, optional
        namespace object type belongs to, by default "http://iec.ch/TC57/2013/CIM-schema-cim16#"

    Returns
    -------
    int
       Number of instances of given object type in list of xml root elements
    """

    tag_name = f"{{{namespace}}}{object_type}"
    count = 0
    for child in xml_root_elements:
        if tag_name in child.tag:
            count += 1
    return count



def get_object_types(xml_root_elements: list) -> list:
    """Get all object types from list of xml root elements

    Parameters
    ----------
    xml_root_elements : list
        List of xml root elements

    Returns
    -------
    list
       List of object types
    """
    object_types = []
    for child in xml_root_elements:
        object_type = child.tag

        if object_type not in object_types:
            object_types.append(object_type)

    return object_types


def get_counts_per_object_types(xml_root_elements: list) -> dict[str,int]:
    """Get object types and their counts

    Parameters
    ----------
    xml_root_elements : list
       List of xml root elements

    Returns
    -------
    dict
        Dictionary of object types as keys and counts as values
    """
    count = {}
    for child in xml_root_elements:
        object_type = child.tag.split("}")[1]
        if object_type not in count:
            count[object_type] = 1
        else:
            count[object_type] += 1
    return count



def get_instance_id_and_name(xml_root_elements: list, object_type: str, namespace: str = "http://iec.ch/TC57/2013/CIM-schema-cim16#" ) -> dict:
    """Get object type instance id and name

    Parameters
    ----------
    xml_root_elements : list
        List of xml root elements
    object_type : str
        Name of object type
    namespace : str, optional
        namespace object type belongs to, by default "http://iec.ch/TC57/2013/CIM-schema-cim16#"

    Returns
    -------
    dict
        Dictionary with object type instances ids as  keys, and object type instances names as values
    """

    tag_name = f"{{{namespace}}}{object_type}"
    identified_object_name = f"{{{namespace}}}IdentifiedObject.name"
    instances_dict = {}
    for child in xml_root_elements:
        if tag_name in child.tag:
            for child_child in child:
                if identified_object_name in child_child.tag:
                    instances_dict[child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID"]] = child_child.text
    return instances_dict


def get_all_ac_line_segments(xml_root_elements: list, object_type: str, namespace: str = "http://iec.ch/TC57/2013/CIM-schema-cim16#" ) -> dict[str, ACLineSegment]:
    """Get all AC Line segment instances from the list of xml root elements

    Parameters
    ----------
    xml_root_elements : list
        List of xml root elements
    object_type : str
        Name of object type
    namespace : str, optional
        namespace object type belongs to, by default "http://iec.ch/TC57/2013/CIM-schema-cim16#"

    Returns
    -------
    dict[str, ACLineSegment]
        Dictionary with AC Line Segment instances ids as keys, and ACLine Segment class instances as values
    """
    object_type_uri = f"{{{namespace}}}{object_type}"
    rdf_ID_uri = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID"
    name_property_uri = f"{{{namespace}}}IdentifiedObject.name"
    resistance_property_uri = f"{{{namespace}}}ACLineSegment.r"

    ac_line_segments = {}

    for child in xml_root_elements:
        if object_type_uri in child.tag:
            rdf_ID = child.attrib[rdf_ID_uri]
            for child_child in child:
                if name_property_uri in child_child.tag:
                    name = child_child.text
                if resistance_property_uri in child_child.tag:
                    resistance = child_child.text
            ac_line_segments[rdf_ID] = ACLineSegment(name = name, rdf_ID = rdf_ID, resistance = resistance)
    return ac_line_segments



def get_all_substations(xml_root_elements: list, object_type: str, namespace: str = "http://iec.ch/TC57/2013/CIM-schema-cim16#" ) -> dict[str, Substation]:
    """Get all Substation instances from the list of xml root elements

    Parameters
    ----------
    xml_root_elements : list
        List of xml root elements
    object_type : str
        Name of object type
    namespace : str, optional
        namespace object type belongs to, by default "http://iec.ch/TC57/2013/CIM-schema-cim16#"

    Returns
    -------
    dict[str, Substation]
        Dictionary with Substation instances ids as keys, and Substation class instances as values
    """
    object_type_uri = f"{{{namespace}}}{object_type}"
    rdf_ID_uri = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}ID"
    region_property_uri = f"{{{namespace}}}Substation.Region"
    name_property = f"{{{namespace}}}IdentifiedObject.name"

    substations = {}

    for child in xml_root_elements:
        if object_type_uri in child.tag:
            rdf_ID = child.attrib[rdf_ID_uri]

            for child_child in child:
                if region_property_uri in child_child.tag:
                    region_property = child_child.attrib["{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"]

                if name_property in child_child.tag:
                    name = child_child.text
            substations[rdf_ID] = Substation(rdf_ID = rdf_ID, region = region_property, name = name)

    return substations
