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
		log.Fatal("Usage: go run nature_nurture_summary.go data/nature_nurture_development_panel.csv")
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
	scoreIdx := col(header, "development_score")
	protectiveIdx := col(header, "protective_context")
	supportIdx := col(header, "caregiver_support")
	stressIdx := col(header, "acute_stress")
	sensitivityIdx := col(header, "biological_sensitivity")
	riskIdx := col(header, "structural_risk")
	if scoreIdx < 0 || protectiveIdx < 0 || supportIdx < 0 || stressIdx < 0 || sensitivityIdx < 0 || riskIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	scoreSum, protectiveSum, supportSum, stressSum, sensitivitySum, riskSum := 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		score, e1 := strconv.ParseFloat(row[scoreIdx], 64)
		protective, e2 := strconv.ParseFloat(row[protectiveIdx], 64)
		support, e3 := strconv.ParseFloat(row[supportIdx], 64)
		stress, e4 := strconv.ParseFloat(row[stressIdx], 64)
		sensitivity, e5 := strconv.ParseFloat(row[sensitivityIdx], 64)
		risk, e6 := strconv.ParseFloat(row[riskIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil || e6 != nil {
			continue
		}
		count++
		scoreSum += score
		protectiveSum += protective
		supportSum += support
		stressSum += stress
		sensitivitySum += sensitivity
		riskSum += risk
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(count))
	fmt.Printf("Mean protective_context: %.4f\n", protectiveSum/float64(count))
	fmt.Printf("Mean caregiver_support: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean acute_stress: %.4f\n", stressSum/float64(count))
	fmt.Printf("Mean biological_sensitivity: %.4f\n", sensitivitySum/float64(count))
	fmt.Printf("Mean structural_risk: %.4f\n", riskSum/float64(count))
}
