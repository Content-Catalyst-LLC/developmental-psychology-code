package main
import (
  "encoding/csv"; "fmt"; "log"; "os"; "strconv"
)
func idx(h []string, name string) int { for i,v := range h { if v == name { return i } }; return -1 }
func main() {
  if len(os.Args) < 2 { log.Fatal("usage: go run adolescence_identity_summary.go data/adolescence_identity_panel.csv") }
  f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
  rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
  h := rows[0]; s:=idx(h,"identity_score"); c:=idx(h,"support_context"); x:=idx(h,"current_exclusion"); d:=idx(h,"digital_stress")
  n:=0; ss:=0.0; cc:=0.0; xx:=0.0; dd:=0.0
  for _, r := range rows[1:] { a,_:=strconv.ParseFloat(r[s],64); b,_:=strconv.ParseFloat(r[c],64); e,_:=strconv.ParseFloat(r[x],64); g,_:=strconv.ParseFloat(r[d],64); n++; ss+=a; cc+=b; xx+=e; dd+=g }
  fmt.Printf("Rows analyzed: %d\\nMean identity_score: %.4f\\nMean support_context: %.4f\\nMean current_exclusion: %.4f\\nMean digital_stress: %.4f\\n", n, ss/float64(n), cc/float64(n), xx/float64(n), dd/float64(n))
}
