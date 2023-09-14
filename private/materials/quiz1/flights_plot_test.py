example_row = {k.lower(): v for k, v in example_row.items()}
print("Keys:", sorted(example_row.keys()))
print("`hour` is numeric:", isinstance(example_row["hour"], (int, float)))
print("`mean_delay` is numeric:", isinstance(example_row["mean_delay"], (int, float)))
print("`origin` is one of the valid options:", example_row['origin'].upper() in ["EWR", "JFK", "LGA"])