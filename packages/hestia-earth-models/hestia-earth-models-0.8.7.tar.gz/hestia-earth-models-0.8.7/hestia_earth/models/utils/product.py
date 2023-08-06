from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match, linked_node
from hestia_earth.utils.tools import list_average, list_sum, safe_parse_float

from . import _term_id, _include_methodModel
from .property import get_node_property


def _new_product(term, model=None):
    node = {'@type': SchemaType.PRODUCT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def _get_nitrogen_content(product: dict):
    return safe_parse_float(
        get_node_property(product, 'nitrogenContent').get('value', 0)) if product else 0


def _get_nitrogen_tan_content(product: dict):
    return safe_parse_float(
        get_node_property(product, 'totalAmmoniacalNitrogenContentAsN').get('value', 0)) if product else 0


def abg_total_residue_nitrogen(products: list):
    """
    Get the total above ground nitrogen content from the `aboveGroundCropResidueTotal` product.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    return _get_nitrogen_content(find_term_match(products, 'aboveGroundCropResidueTotal'))


def total_excreta_tan(products: list):
    """
    Get the total excreta ammoniacal nitrogen from all the products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    excreta = find_term_match(products, 'excretaKgMass').get('value', [0])
    excreta_as_n = find_term_match(products, 'excretaAsN').get('value', [0])
    excreta_tan_content = _get_nitrogen_tan_content(find_term_match(products, 'excretaKgMass'))
    excreta_as_n_tan_content = _get_nitrogen_tan_content(find_term_match(products, 'excretaAsN'))
    return (list_sum(excreta) * excreta_tan_content + list_sum(excreta_as_n) * excreta_as_n_tan_content) / 100


def total_excreta_n(products: list):
    """
    Get the total excreta nitrogen from all the products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    excreta = find_term_match(products, 'excretaKgMass').get('value', [0])
    excreta_as_n = find_term_match(products, 'excretaAsN').get('value', [0])
    excreta_nitrogen_content = _get_nitrogen_content(find_term_match(products, 'excretaKgMass'))
    return list_sum(excreta_as_n) + list_sum(excreta) * excreta_nitrogen_content / 100


def abg_residue_nitrogen(products: list):
    """
    Get the total nitrogen content from all the `aboveGroundCropResidue` products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    left_on_field = find_term_match(products, 'aboveGroundCropResidueLeftOnField').get('value', [0])
    incorporated = find_term_match(products, 'aboveGroundCropResidueIncorporated').get('value', [0])
    return list_sum(left_on_field + incorporated) * abg_total_residue_nitrogen(products) / 100


def blg_residue_nitrogen(products: list):
    """
    Get the total nitrogen content from the `belowGroundCropResidue` product.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    residue = find_term_match(products, 'belowGroundCropResidue')
    return list_sum(residue.get('value', [0])) * _get_nitrogen_content(residue) / 100


def residue_nitrogen(products: list) -> float:
    """
    Get the total nitrogen content from the `cropResidue` products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    return abg_residue_nitrogen(products) + blg_residue_nitrogen(products)


def get_average_rooting_depth(cycle: dict) -> float:
    properties = list(map(lambda p: get_node_property(p, 'rootingDepth'), cycle.get('products', [])))
    return list_average([
        safe_parse_float(p.get('value')) for p in properties if p.get('value') is not None
    ])
