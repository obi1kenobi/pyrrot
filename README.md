# Pyrrot

This is a set of tools developed for use with an Parrot AR.Drone 2.0, as part of 16.S685 Crash Course in Autonomy.

## Requirements

This project uses the Shapely geometric library.

## Scripts

To convert CSV feature and obstacle lists into YAML environments suitable for simulations:
```bash
python csv_to_yaml.py <csv_obstacles> <csv_features> <yaml_output>
```
