#No need for outcome values therefore I did not take it
data1 = [6,148,72,35,0,33.6,0.627,50]
data2 = [1,85,66,29,0,26.6,0.351,31]

result = 0

data1.zip(data2).each do |val1, val2|
  result += (val1 - val2) ** 2
end

puts "Distance before sqrt: #{result}"

result = Math.sqrt(result)
puts "Distance: #{result}"
