package main
import ("encoding/csv"; "fmt"; "log"; "os"; "strconv")
func idx(h []string, name string) int { for i,v := range h { if v == name { return i } }; return -1 }
func main() {
  if len(os.Args) < 2 { log.Fatal("usage: go run puberty_summary.go data/puberty_embodiment_panel.csv") }
  f, err := os.Open(os.Args[1]); if err != nil { log.Fatal(err) }; defer f.Close()
  rows, err := csv.NewReader(f).ReadAll(); if err != nil { log.Fatal(err) }
  h := rows[0]; s:=idx(h,"adjustment_score"); c:=idx(h,"protective_context"); x:=idx(h,"current_stigma"); b:=idx(h,"current_body_concern"); p:=idx(h,"current_peer_comparison")
  n:=0; ss:=0.0; cc:=0.0; xx:=0.0; bb:=0.0; pp:=0.0
  for _, r := range rows[1:] { a,_:=strconv.ParseFloat(r[s],64); d,_:=strconv.ParseFloat(r[c],64); e,_:=strconv.ParseFloat(r[x],64); g,_:=strconv.ParseFloat(r[b],64); q,_:=strconv.ParseFloat(r[p],64); n++; ss+=a; cc+=d; xx+=e; bb+=g; pp+=q }
  fmt.Printf("Rows analyzed: %d\nMean adjustment_score: %.4f\nMean protective_context: %.4f\nMean current_stigma: %.4f\nMean current_body_concern: %.4f\nMean current_peer_comparison: %.4f\n", n, ss/float64(n), cc/float64(n), xx/float64(n), bb/float64(n), pp/float64(n))
}
