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
		log.Fatal("Usage: go run aging_adaptation_summary.go data/aging_adaptation_later_life_panel.csv")
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
	fitIdx := col(header, "functional_fit")
	supportIdx := col(header, "current_support")
	healthIdx := col(header, "current_health")
	adaptationIdx := col(header, "current_adaptation")
	if adjustmentIdx < 0 || fitIdx < 0 || supportIdx < 0 || healthIdx < 0 || adaptationIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	adjustmentSum, fitSum, supportSum, healthSum, adaptationSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		adjustment, e1 := strconv.ParseFloat(row[adjustmentIdx], 64)
		fit, e2 := strconv.ParseFloat(row[fitIdx], 64)
		support, e3 := strconv.ParseFloat(row[supportIdx], 64)
		health, e4 := strconv.ParseFloat(row[healthIdx], 64)
		adaptation, e5 := strconv.ParseFloat(row[adaptationIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		adjustmentSum += adjustment
		fitSum += fit
		supportSum += support
		healthSum += health
		adaptationSum += adaptation
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean adjustment_score: %.4f\n", adjustmentSum/float64(count))
	fmt.Printf("Mean functional_fit: %.4f\n", fitSum/float64(count))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean current_health: %.4f\n", healthSum/float64(count))
	fmt.Printf("Mean current_adaptation: %.4f\n", adaptationSum/float64(count))
}
