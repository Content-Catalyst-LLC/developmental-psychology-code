package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

func idx(h []string, name string) int {
	for i, v := range h {
		if v == name {
			return i
		}
	}
	return -1
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("usage: go run developmental_summary.go data/developmental_lifespan_panel.csv")
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

	h := rows[0]
	score := idx(h, "development_score")
	protective := idx(h, "protective_context")
	support := idx(h, "current_support")
	stress := idx(h, "acute_stress")
	intervention := idx(h, "intervention")

	n := 0
	scoreSum, protectiveSum, supportSum, stressSum, interventionSum := 0.0, 0.0, 0.0, 0.0, 0.0

	for _, r := range rows[1:] {
		vScore, _ := strconv.ParseFloat(r[score], 64)
		vProtective, _ := strconv.ParseFloat(r[protective], 64)
		vSupport, _ := strconv.ParseFloat(r[support], 64)
		vStress, _ := strconv.ParseFloat(r[stress], 64)
		vIntervention, _ := strconv.ParseFloat(r[intervention], 64)
		n++
		scoreSum += vScore
		protectiveSum += vProtective
		supportSum += vSupport
		stressSum += vStress
		interventionSum += vIntervention
	}

	fmt.Printf("Rows analyzed: %d\n", n)
	fmt.Printf("Mean development_score: %.4f\n", scoreSum/float64(n))
	fmt.Printf("Mean protective_context: %.4f\n", protectiveSum/float64(n))
	fmt.Printf("Mean current_support: %.4f\n", supportSum/float64(n))
	fmt.Printf("Mean acute_stress: %.4f\n", stressSum/float64(n))
	fmt.Printf("Mean intervention: %.4f\n", interventionSum/float64(n))
}
