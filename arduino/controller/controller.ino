

// Electrode 
int pin_electrode_1_current = 9; // Needs to be a PWM pin to be able to control motor speed
int pin_electrode_1_polarity_A = 2;
int pin_electrode_1_polarity_B = 3;
// Electrode 2
int pin_electrode_2_current = 10; 
int pin_electrode_2_polarity_A = 4;
int pin_electrode_2_polarity_B = 5;

int electrode_1_polarity = LOW;
int electrode_2_polarity = LOW;
  
int electrode_1_current = 255;
int electrode_2_current = 255;

String InBuffer;

void setup() {
  // initialize serial communication @ 9600 baud:
  Serial.begin(9600);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(pin_electrode_1_polarity_A,OUTPUT);
  pinMode(pin_electrode_1_polarity_B,OUTPUT);
  pinMode(pin_electrode_1_current,OUTPUT);

  pinMode(pin_electrode_2_polarity_A,OUTPUT);
  pinMode(pin_electrode_2_polarity_B,OUTPUT);
  pinMode(pin_electrode_2_current,OUTPUT);

  analogWrite(pin_electrode_1_current,255);
  analogWrite(pin_electrode_2_current,255);
  digitalWrite(pin_electrode_1_polarity_A,LOW);
  digitalWrite(pin_electrode_1_polarity_B,HIGH);
  
  digitalWrite(pin_electrode_2_polarity_A,LOW);
  digitalWrite(pin_electrode_2_polarity_B,HIGH);

  Serial.begin(9600);
}

void loop() {
  //allowed values are 0 or 1 for polarity

   
    while (Serial.available() > 0)  // While there is something in the Serial buffer
    {

      char Incoming = Serial.read();
      InBuffer += Incoming;  // Concatonates individual characters from buffer into meaningful string

      if(Incoming == '\n') {  // Signifies end of stream from Python

        electrode_1_polarity = InBuffer.substring(0,1).toInt();
        electrode_2_polarity = InBuffer.substring(1,2).toInt();
        electrode_1_current = InBuffer.substring(2,5).toInt(); 
        electrode_2_current = InBuffer.substring(5,8).toInt(); 
        
        InBuffer = ""; // This resets the buffer
      }
          
    }

         
    


  //write currents
  analogWrite(pin_electrode_1_current,electrode_1_current);
  analogWrite(pin_electrode_2_current,electrode_2_current);
  //write polarities
  if (electrode_1_polarity == 0){
    digitalWrite(pin_electrode_1_polarity_A,LOW);
    digitalWrite(pin_electrode_1_polarity_B,HIGH);
  }else{
    digitalWrite(pin_electrode_1_polarity_A,HIGH);
    digitalWrite(pin_electrode_1_polarity_B,LOW);
  }
  
  if (electrode_2_polarity == 0){
    digitalWrite(pin_electrode_2_polarity_A,LOW);
    digitalWrite(pin_electrode_2_polarity_B,HIGH);
  }else{
    digitalWrite(pin_electrode_2_polarity_A,HIGH);
    digitalWrite(pin_electrode_2_polarity_B,LOW);
  }
  //wait
  delay(100);
  
  

}
