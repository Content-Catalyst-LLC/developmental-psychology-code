package main
import ("encoding/csv"; "fmt"; "log"; "os"; "strconv")
func idx(h []string, name string) int { for i, v := range h { if v == name { return i } }; return -1 }
func main() {
 if len(os.Args) < 2 { log.Fatal("usage: go run brain_development_summary.go data/brain_development_panel.csv") }
 f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
 rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
 h := rows[0]
 cols := []int{idx(h,"neural_state"),idx(h,"developmental_outcome"),idx(h,"acute_stress"),idx(h,"developmental_support_context")}
 names := []string{"neural_state","developmental_outcome","acute_stress","developmental_support_context"}
 sums := make([]float64, len(cols))
 for _, r := range rows[1:] { for j, c := range cols { v, _ := strconv.ParseFloat(r[c], 64); sums[j] += v } }
 fmt.Printf("Rows analyzed: %d\n", len(rows)-1)
 for j, name := range names { fmt.Printf("Mean %s: %.4f\n", name, sums[j]/float64(len(rows)-1)) }
}
