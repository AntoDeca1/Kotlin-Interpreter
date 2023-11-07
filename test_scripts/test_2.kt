fun main() {
    var z: Int = 12
    var x: String = "Prova"
    var k: Int = 5 + 5 * z
    k=40;
    print(x + k)
    if (k > 20 && z < k) {
        print("Complimenti")
    }
    while (k > 20) {
        print(k)
        k = k - 4
    }
    fun sum(x:Int,y:Int):Int{
          return x+y
          }

    for(i in z..15){
        print(i)
    }
    print("-----Comparison Operators-----")
    print(z+3==15)
    print(z>=15)
    print(z<=15)
    print(!(z>=15))
    print("----Operation with functions-----")
    val final_variable= sum(4,2) + 3 + sum(2,1)
    print(final_variable)

}

