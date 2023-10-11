fun main() {
    var z: Int = 12
    var x: String = "Prova"
    var k: Int = 5 + 5 * z
    k = k - 40
    print(x + k)
    if (k > 20 && z < k) {
        print("Complimenti")
    }
    while (k > 20) {
        print(k)
        k = k - 4
    }

    for(i in z..15){
        print(i)
    }

}

