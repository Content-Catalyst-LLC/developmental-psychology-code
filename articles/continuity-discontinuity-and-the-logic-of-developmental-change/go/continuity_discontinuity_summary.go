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
		log.Fatal("Usage: go run continuity_discontinuity_summary.go data/continuity_discontinuity_panel.csv")
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
	readinessIdx := col(header, "transition_readiness")
	supportIdx := col(header, "current_support")
	stressIdx := col(header, "chronic_stress")
	ruptureIdx := col(header, "institutional_rupture")
	interventionIdx := col(header, "intervention_exposure")
	if scoreIdx < 0 || readinessIdx < 0 || supportIdx < 0 || stressIdx < 0 || ruptureIdx < 0 || interventionIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	scoreSum, readinessSum, supportSum, stressSum, ruptureSum, interventionSum := 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		score, e1 := strconv.ParseFloat(row[scoreIdx], 64)
		readiness, e2 := strconv.ParseFloat(row[readinessIdx], 64)
		support, e3 := strconv.ParseFloat(row[supportIdx], 64)
		stress, e4 := strconv.ParseFloat(row[stressIdx], 64)
		rupture, e5 := strconv.ParseFloat(row[ruptureIdx], 64)
		intervention, e6 := strconv.ParseFloat(row[interventionIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil || e6 != nil {
			continue
		}
		count++
		scoreSum += score
		readinessSum += readiness
		supportSum += support
		stressSum += stress
		ruptureSum += rupture
		interventionSum += intervention
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(count))
	fmt.Printf("Mean transition_readiness: %.4f\n", readinessSum/float64(count))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(count))
	fmt.Printf("Mean chronic_stress: %.4f\n", stressSum/float64(count))
	fmt.Printf("Mean institutional_rupture: %.4f\n", ruptureSum/float64(count))
	fmt.Printf("Mean intervention_exposure: %.4f\n", interventionSum/float64(count))
}
