val u=20;
fun main() {
    val x = 5
    var y = 10
    for (i in 1..4){
        for(j in 1..5 step 2){
        y=y+1
        }
    }
    print(u)
    while(y<280){
     y=y+1}
    print("----Variabile y dopo le modifiche----")
    print(y)
    print("----Variabile k dichiarata come una operazione complessa----")
    val k= (x+20)*10+20
    print(k)
    if(k >20){
    print("Complimenti")
    }
    else{
    }
    val z = readLine()
    print(z)
}
