#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  python3 - <<PY
import pandas as pd
df1 = pd.DataFrame({"A": ["x", "y", "z"], "B": [1, 2, 3]})
df2 = pd.DataFrame({"A": ["x", "y", "Z"], "B": [1, 2, 4]})
df1.to_excel("tmp/old.xlsx", index=False)
df2.to_excel("tmp/new.xlsx", index=False)
PY
}

teardown() {
  rm -rf tmp
}

@test "excel_diff detects differences" {
  run ./bin/shellman excel_diff tmp/old.xlsx tmp/new.xlsx
  echo "OUTPUT: $output"
  echo "STATUS: $status"
  [ "$status" -eq 0 ]
  [[ "$output" =~ "Z" ]]
}
