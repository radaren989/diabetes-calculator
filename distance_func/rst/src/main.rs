
fn main() {
    //No need for outcome values therefore I did not take it
    let data1: [f64; 8] = [6.0,148.0,72.0,35.0,0.0,33.6,0.627,50.0];
    let data2: [f64; 8] = [1.0,85.0,66.0,29.0,0.0,26.6,0.351,31.0];
    
    let mut result: f64 = 0.0;

    for (val1, val2) in data1.iter().zip(data2.iter()){
        result += (val1 - val2).powi(2);
    }
    
    println!("Distance before sqrt: {}", result);

    result = result.sqrt();

    println!("Distance: {}", result);
}

