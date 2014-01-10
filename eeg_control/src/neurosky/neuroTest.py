from NeuroPy import NeuroPy
object1=NeuroPy("/dev/ttyUSB0")
def attention_callback(attention_value):
    "this function will be called everytime NeuroPy has a new value for attention"
    print "Value of attention is",attention_value
        #do other stuff (fire a rocket), based on the obtained value of attention_value
        #do some more stuff
    return None

object1.setCallBack("attention",attention_callback)

object1.start()

while True:
    if(object1.meditation>70): #another way of accessing data provided by headset (1st being call backs)
        object1.stop()         #if meditation level reaches above 70, stop fetching data from the headset
 
