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
		log.Fatal("Usage: go run culture_summary.go data/cultural_development_panel.csv")
	}

	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	rows, err := csv.NewReader(file).ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	if len(rows) < 2 {
		log.Fatal("CSV has no data rows")
	}

	header := rows[0]
	scoreIdx := findColumn(header, "development_score")
	mismatchIdx := findColumn(header, "current_mismatch")
	supportIdx := findColumn(header, "current_support")

	if scoreIdx < 0 || mismatchIdx < 0 || supportIdx < 0 {
		log.Fatal("Required columns not found")
	}

	count := 0
	scoreSum := 0.0
	mismatchSum := 0.0
	supportSum := 0.0

	for _, row := range rows[1:] {
		score, err1 := strconv.ParseFloat(row[scoreIdx], 64)
		mismatch, err2 := strconv.ParseFloat(row[mismatchIdx], 64)
		support, err3 := strconv.ParseFloat(row[supportIdx], 64)

		if err1 != nil || err2 != nil || err3 != nil {
			continue
		}

		count++
		scoreSum += score
		mismatchSum += mismatch
		supportSum += support
	}

	if count == 0 {
		log.Fatal("No valid rows found")
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(count))
	fmt.Printf("Mean current_mismatch: %.4f\n", mismatchSum/float64(count))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(count))
}
