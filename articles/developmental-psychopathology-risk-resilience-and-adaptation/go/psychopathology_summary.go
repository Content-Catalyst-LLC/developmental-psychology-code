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
		log.Fatal("Usage: go run psychopathology_summary.go data/developmental_psychopathology_panel.csv")
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
	adaptIdx := col(header, "adaptation_score")
	riskIdx := col(header, "current_risk")
	supportIdx := col(header, "current_support")
	if adaptIdx < 0 || riskIdx < 0 || supportIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	adaptSum, riskSum, supportSum := 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		adapt, e1 := strconv.ParseFloat(row[adaptIdx], 64)
		risk, e2 := strconv.ParseFloat(row[riskIdx], 64)
		support, e3 := strconv.ParseFloat(row[supportIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil {
			continue
		}
		count++
		adaptSum += adapt
		riskSum += risk
		supportSum += support
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean adaptation_score: %.4f\n", adaptSum/float64(count))
	fmt.Printf("Mean current_risk: %.4f\n", riskSum/float64(count))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(count))
}
