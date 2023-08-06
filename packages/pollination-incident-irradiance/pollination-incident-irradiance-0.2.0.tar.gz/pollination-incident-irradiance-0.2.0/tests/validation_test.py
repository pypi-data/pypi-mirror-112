from pollination.incident_irradiance.entry import IncidentIrradianceEntryPoint
from queenbee.recipe.dag import DAG


def test_incident_irradiance():
    recipe = IncidentIrradianceEntryPoint().queenbee
    assert recipe.name == 'incident-irradiance-entry-point'
    assert isinstance(recipe, DAG)
