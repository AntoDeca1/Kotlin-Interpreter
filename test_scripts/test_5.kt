fun main(){
    fun prova(x:Int){
        print(x)
    }

    fun prova2(x:Int,y:Int){
        return x + y
    }
    prova(5)
    print(prova2(5,4))
    prova()
}