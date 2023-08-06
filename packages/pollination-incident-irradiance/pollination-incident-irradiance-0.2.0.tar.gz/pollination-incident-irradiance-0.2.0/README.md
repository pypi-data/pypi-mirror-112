# Incident Irradiance

Incident irradiance recipe for Pollination

This recipe calculates the incident irradiance for each time step provided by a wea file.
The outputs are stored under `results/direct` and `results/total`. Nighttime hours are
filtered before running the simulation. To match the results for each of the hours,
see the list of hours in sun-up-hours.txt.

## Methods

This recipe calculates the total amount of Radiation by calculating the direct sunlight
radiation from sun disks and adding them to the contribution from indirect sky radiation.

```console
incident_radiation = direct_sun_radiation + indirect_sky_radiation
```

The recipe is structured in a manner that ambient bounces are not included.
