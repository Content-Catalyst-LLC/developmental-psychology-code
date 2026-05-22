package main
import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)
func idx(h []string, name string) int { for i, v := range h { if v == name { return i } }; return -1 }
func main() {
	if len(os.Args) < 2 { log.Fatal("usage: go run social_development_summary.go data/social_development_panel.csv") }
	f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
	rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
	h := rows[0]
	cols := []int{idx(h,"social_self_score"),idx(h,"social_support_context"),idx(h,"current_exclusion"),idx(h,"bullying_exposure"),idx(h,"digital_comparison_stress")}
	names := []string{"social_self_score","social_support_context","current_exclusion","bullying_exposure","digital_comparison_stress"}
	sums := make([]float64, len(cols))
	for _, r := range rows[1:] { for j, c := range cols { v, _ := strconv.ParseFloat(r[c], 64); sums[j] += v } }
	fmt.Printf("Rows analyzed: %d\n", len(rows)-1)
	for j, name := range names { fmt.Printf("Mean %s: %.4f\n", name, sums[j]/float64(len(rows)-1)) }
}
