package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func col(header []string, name string) int {
	for i, h := range header {
		if h == name {
			return i
		}
	}
	return -1
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run adult_development_summary.go data/adult_development_life_stages_panel.csv")
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	rows, err := csv.NewReader(f).ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	if len(rows) < 2 {
		log.Fatal("CSV has no data rows")
	}

	header := rows[0]
	adjustmentIdx := col(header, "adjustment_score")
	supportIdx := col(header, "current_relational_support")
	workIdx := col(header, "current_work_integration")
	healthIdx := col(header, "current_health_burden")
	burdenIdx := col(header, "current_role_burden")
	if adjustmentIdx < 0 || supportIdx < 0 || workIdx < 0 || healthIdx < 0 || burdenIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	adjustmentSum, supportSum, workSum, healthSum, burdenSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		adjustment, e1 := strconv.ParseFloat(row[adjustmentIdx], 64)
		support, e2 := strconv.ParseFloat(row[supportIdx], 64)
		work, e3 := strconv.ParseFloat(row[workIdx], 64)
		health, e4 := strconv.ParseFloat(row[healthIdx], 64)
		burden, e5 := strconv.ParseFloat(row[burdenIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		adjustmentSum += adjustment
		supportSum += support
		workSum += work
		healthSum += health
		burdenSum += burden
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean adjustment_score: %.4f\n", adjustmentSum/float64(count))
	fmt.Printf("Mean current_relational_support: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean current_work_integration: %.4f\n", workSum/float64(count))
	fmt.Printf("Mean current_health_burden: %.4f\n", healthSum/float64(count))
	fmt.Printf("Mean current_role_burden: %.4f\n", burdenSum/float64(count))
}
