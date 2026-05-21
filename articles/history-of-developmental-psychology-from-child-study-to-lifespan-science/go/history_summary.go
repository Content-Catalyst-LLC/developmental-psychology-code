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
		log.Fatal("usage: go run history_summary.go data/developmental_psychology_history_panel.csv")
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
	b := idx(h, "broadening_index")
	l := idx(h, "lifespan_index")
	e := idx(h, "ecological_systems_index")
	c := idx(h, "critique_index")

	n := 0
	sb, sl, se, sc := 0.0, 0.0, 0.0, 0.0
	for _, r := range rows[1:] {
		vb, _ := strconv.ParseFloat(r[b], 64)
		vl, _ := strconv.ParseFloat(r[l], 64)
		ve, _ := strconv.ParseFloat(r[e], 64)
		vc, _ := strconv.ParseFloat(r[c], 64)
		n++
		sb += vb
		sl += vl
		se += ve
		sc += vc
	}

	fmt.Printf("Rows analyzed: %d\n", n)
	fmt.Printf("Mean broadening_index: %.4f\n", sb/float64(n))
	fmt.Printf("Mean lifespan_index: %.4f\n", sl/float64(n))
	fmt.Printf("Mean ecological_systems_index: %.4f\n", se/float64(n))
	fmt.Printf("Mean critique_index: %.4f\n", sc/float64(n))
}
