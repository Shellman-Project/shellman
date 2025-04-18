#!/usr/bin/env bats

setup() {
  mkdir -p tmp
  cat > tmp/sample.csv <<'EOF'
id,name,status
1,Alice,OK
2,Bob,ERROR
3,Carol,OK
4,Dan,ERROR
EOF
}

teardown() {
  rm -rf tmp
}

@test "extracts chosen columns and rows" {
  run ./bin/shellman csv_extract tmp/sample.csv --cols 1,3 --rows 2-3 --skip-header
  [ "$status" -eq 0 ]

  csv_lines=$(echo "$output" | grep -E '^[0-9]+,')
  line_count=$(echo "$csv_lines" | wc -l)
  [ "$line_count" -eq 2 ]

  [[ "$csv_lines" == "2,ERROR"* ]]
  [[ "$csv_lines" == *$'\n'"3,OK" ]]
}


@test "filters rows containing text and saves to file" {
  run ./bin/shellman csv_extract tmp/sample.csv --cols 2 --contains ERROR --output tmp/errors.csv --skip-header
  [ "$status" -eq 0 ]
  [ -f tmp/errors.csv ]

  names=$(cat tmp/errors.csv)
  [[ "$names" == "Bob"$'\n'"Dan" ]]
}
