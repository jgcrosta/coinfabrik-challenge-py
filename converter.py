# Load cg_data.csv and convert everything into a TypeScript object, then save it as cg_data.ts. The result should be an object with the Interface "LatestResponse":
# export interface LatestResponse {
#   data: Data[];
# }
# export interface Data {
#   name: string;
#   symbol: string;
#   market_cap: number;
#   volume_24h: number;
# }
#

import pandas as pd
import json

# Load cg_data.csv
cg_df = pd.read_csv("cg_data.csv")

# Convert cg_df to a dictionary
cg_dict = cg_df.to_dict(orient="records")

# Convert cg_dict to a JSON string
cg_json = json.dumps(cg_dict)

# Convert cg_json to a TypeScript object
cg_ts = f"export const cg_data: LatestResponse = {cg_json};"

# Save cg_ts to a file
with open("cg_data.ts", "w") as f:
    f.write(cg_ts)
