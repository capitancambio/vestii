

// Electrode 1
int pin_electrode_1_polarity = 2;
int pin_electrode_1_current = 9; // Needs to be a PWM pin to be able to control motor speed

// Electrode 2
int pin_electrode_2_polarity = 4;
int pin_electrode_2_current = 10; // Needs to be a PWM pin to be able to control motor speed


void setup() {
  // initialize serial communication @ 9600 baud:
  Serial.begin(9600);

  //Define L298N Dual H-Bridge Motor Controller Pins

  pinMode(pin_electrode_1_polarity,OUTPUT);
  pinMode(pin_electrode_1_current,OUTPUT);
  pinMode(pin_electrode_2_polarity,OUTPUT);
  pinMode(pin_electrode_2_current,OUTPUT);

  analogWrite(pin_electrode_1_current,0);
  analogWrite(pin_electrode_2_current,0);
  digitalWrite(pin_electrode_1_polarity,LOW);
  digitalWrite(pin_electrode_2_polarity,LOW);

  Serial.begin(9600);
}

void loop() {
  int electrode_1_polarity = LOW;
  int electrode_2_polarity = LOW;
  
  int electrode_1_current = 0;
  int electrode_2_current = 0;


  while (Serial.available() > 0)  // While there is something in the Serial buffer   // Maybe serial isn't available
    {

      char Incoming = Serial.read();
      InBuffer += Incoming;  // Concatonates individual characters from buffer into meaningful string

      if(Incoming == '\n') {
        CharNum = InBuffer.indexOf('#');
        Sub1 = InBuffer.substring(0, CharNum);
        Sub2 = InBuffer.substring((CharNum + 1));
        CharNum2 = Sub2.indexOf('\\');
        Sub3 = Sub2.substring(0,CharNum2);
        TaxelID = ((Sub3.toInt()) + 1);
        Angle = Sub1.toInt();

        ServoArray[TaxelID].attach(TaxelID);
        ServoArray[TaxelID].write(Angle);


        InBuffer = ""; // This resets the buffer
          }}













  if (Serial.available() > 0) {

  }
  //write currents
  analogWrite(pin_electrode_1_current,electrode_1_current);
  analogWrite(pin_electrode_2_current,electrode_2_current);
  //write polarities
  digitalWrite(pin_electrode_1_polarity,electrode_1_polarity);
  digitalWrite(pin_electrode_2_polarity,electrode_2_polarity);
  //wait
  delay(100);
  
  

}
