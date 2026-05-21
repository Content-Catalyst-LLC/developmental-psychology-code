package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func findColumn(header []string, name string) int {
	for i, col := range header {
		if col == name {
			return i
		}
	}
	return -1
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run timing_summary.go data/developmental_timing_panel.csv")
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rows, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	if len(rows) < 2 {
		log.Fatal("CSV has no data rows")
	}

	header := rows[0]
	criticalIdx := findColumn(header, "critical_outcome")
	sensitiveIdx := findColumn(header, "sensitive_outcome")
	multiIdx := findColumn(header, "multi_window_outcome")

	if criticalIdx < 0 || sensitiveIdx < 0 || multiIdx < 0 {
		log.Fatal("Required outcome columns not found")
	}

	count := 0
	criticalSum := 0.0
	sensitiveSum := 0.0
	multiSum := 0.0

	for _, row := range rows[1:] {
		critical, err1 := strconv.ParseFloat(row[criticalIdx], 64)
		sensitive, err2 := strconv.ParseFloat(row[sensitiveIdx], 64)
		multi, err3 := strconv.ParseFloat(row[multiIdx], 64)

		if err1 != nil || err2 != nil || err3 != nil {
			continue
		}

		count++
		criticalSum += critical
		sensitiveSum += sensitive
		multiSum += multi
	}

	if count == 0 {
		log.Fatal("No valid rows found")
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean critical outcome: %.4f\n", criticalSum/float64(count))
	fmt.Printf("Mean sensitive outcome: %.4f\n", sensitiveSum/float64(count))
	fmt.Printf("Mean multi-window outcome: %.4f\n", multiSum/float64(count))
}
