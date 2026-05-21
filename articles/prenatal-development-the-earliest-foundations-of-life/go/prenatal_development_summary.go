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
		log.Fatal("Usage: go run prenatal_development_summary.go data/prenatal_development_foundations_panel.csv")
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
	outcomeIdx := col(header, "early_outcome")
	careIdx := col(header, "effective_care")
	riskIdx := col(header, "developmental_risk")
	gestationIdx := col(header, "gestational_weeks")
	healthIdx := col(header, "maternal_health")
	if outcomeIdx < 0 || careIdx < 0 || riskIdx < 0 || gestationIdx < 0 || healthIdx < 0 {
		log.Fatal("Required columns missing")
	}

	count := 0
	outcomeSum, careSum, riskSum, gestationSum, healthSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, row := range rows[1:] {
		outcome, e1 := strconv.ParseFloat(row[outcomeIdx], 64)
		care, e2 := strconv.ParseFloat(row[careIdx], 64)
		risk, e3 := strconv.ParseFloat(row[riskIdx], 64)
		gestation, e4 := strconv.ParseFloat(row[gestationIdx], 64)
		health, e5 := strconv.ParseFloat(row[healthIdx], 64)
		if e1 != nil || e2 != nil || e3 != nil || e4 != nil || e5 != nil {
			continue
		}
		count++
		outcomeSum += outcome
		careSum += care
		riskSum += risk
		gestationSum += gestation
		healthSum += health
	}

	fmt.Printf("Rows analyzed: %d\n", count)
	fmt.Printf("Mean early_outcome: %.4f\n", outcomeSum/float64(count))
	fmt.Printf("Mean effective_care: %.4f\n", careSum/float64(count))
	fmt.Printf("Mean developmental_risk: %.4f\n", riskSum/float64(count))
	fmt.Printf("Mean gestational_weeks: %.4f\n", gestationSum/float64(count))
	fmt.Printf("Mean maternal_health: %.4f\n", healthSum/float64(count))
}
