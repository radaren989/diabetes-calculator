package main

import ("fmt";
        "math")

func main(){  
  //No need for outcome values therefore I did not take it
  data1 := [8]float64{6,148,72,35,0,33.6,0.627,50}
  data2 := [8]float64{1,85,66,29,0,26.6,0.351,31}

  var result float64

  for i := 0; i < len(data1); i++{
    result += math.Pow((data1[i] - data2[i]), 2)
  }

  fmt.Println("Distance before sqrt:",result)

  result = math.Sqrt(result)
  fmt.Println("Distance:",result)
}
